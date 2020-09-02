import logging
from typing import Callable, Dict, Any, Union
import requests
from requests.auth import HTTPBasicAuth
from camunda.exceptions import BPMNException, CamundaComputeException
from threading import Timer

DEFAULT_JSON_HEADER = {
    "Content-type": "application/json",
}
DEFAULT_CAMUNDA_URL = "http://localhost:8080/engine-rest"


class ServiceWorker:
    def __init__(
        self,
        base_rest_url: str = DEFAULT_CAMUNDA_URL,
        executors: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {},
        login: str = "",
        password: str = "",
        worker_id: str = "noID",
        retry_time: int = 5,
    ):
        """ ServiceWorker constructor
        Parameters
        ----------
        topic : str
            Camunda topic name
        executor : function Callable[[Dict[str, Any]], Dict[str, Any]]
            A function for executing external tasks
        worker_id : str, optional
            unique worker ID
        base_rest_url : str, optional
            url for Camunda rest API
        retry_time : int, optional
            time for checking new tasks from Camunda in seconds
        """
        self.headers = DEFAULT_JSON_HEADER
        self.base_rest_url = base_rest_url
        self.worker_id = worker_id
        self.login = login
        self.password = password
        self.executors = executors
        self.retry_time = retry_time

    def __fetch_and_lock_tasks(self) -> list:
        topics = []
        for topic in self.executors.keys():
            topics.append({"topicName": topic, "lockDuration": 1000})

        payload = {
            "workerId": self.worker_id,
            "maxTasks": 1,
            "usePriority": True,
            "topics": topics,
        }

        r = requests.post(
            f"{self.base_rest_url}/external-task/fetchAndLock",
            json=payload,
            headers=self.headers,
            auth=HTTPBasicAuth(self.login, self.password),
        )
        r.raise_for_status()
        return r.json()

    def __handle_bpmn_error(self, task, error_code: str):
        payload = {
            "workerId": self.worker_id,
            "errorCode": error_code,
        }
        logging.error(f"BPMN error with task {task['id']} with {error_code}")
        r = requests.post(
            f"{self.base_rest_url}/external-task/{task['id']}/bpmnError",
            json=payload,
            headers=self.headers,
            auth=HTTPBasicAuth(self.login, self.password),
        )
        r.raise_for_status()

    def __handle_compute_error(
        self, task, error_message: str, retries: int = 3, retry_timeout: int = 60000
    ):
        payload = {
            "workerId": self.worker_id,
            "errorMessage": error_message,
            "retries": retries,
            "retryTimeout": retry_timeout,
        }
        logging.error(f"Compute error with task {task['id']} with {error_message}")
        r = requests.post(
            f"{self.base_rest_url}/external-task/{task['id']}/failure",
            json=payload,
            headers=self.headers,
            auth=HTTPBasicAuth(self.login, self.password),
        )
        r.raise_for_status()

    def __complete_task(self, task: dict, variables) -> None:
        payload = {"workerId": self.worker_id, "variables": variables}
        logging.info(f"Complete task {task['id']}")
        r = requests.post(
            f"{self.base_rest_url}/external-task/{task['id']}/complete",
            json=payload,
            headers=self.headers,
            auth=HTTPBasicAuth(self.login, self.password),
        )
        r.raise_for_status()

    def append_executor(
        self, name: str, executor: Callable[[Dict[str, Any]], Dict[str, Any]]
    ) -> None:
        self.executors[name] = executor

    def subscribe(self) -> None:
        logging.info(f"Checking for additional tasks from Camunda")
        try:
            locked_tasks = self.__fetch_and_lock_tasks()
            logging.info(f"Got locked tasks {locked_tasks}")

            for task in locked_tasks:
                try:
                    variables = self.executors[task["topicName"]](task)

                    self.__complete_task(task, variables)
                except BPMNException as err:
                    self.__handle_bpmn_error(task, err.message)
                except CamundaComputeException as err:
                    self.__handle_compute_error(task, err.message)
        except Exception as err:
            logging.error(type(err))
            logging.error(err.args)
            logging.error(err)

        Timer(float(self.retry_time), self.subscribe).start()
