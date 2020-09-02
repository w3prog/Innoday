import os

from worker.executors import (
    fake_executor,
    fake_executor_random
)

executors = {
    "load_data": fake_executor_random,
    "check_completness": fake_executor_random,
    "check_validity": fake_executor_random,
    "check_Uniqueness": fake_executor_random,
    "check_timeliness": fake_executor_random,
    "data_transform": fake_executor_random,
    "generate_report": fake_executor_random,
    "store_data": fake_executor_random,
}


class Config:
    def __init__(self):
        self.log_level = os.getenv("LOG_LEVEL", default="INFO")
        self.camunda_url = os.getenv(
            "CAMUNDA_BASE_REST_API", default="http://localhost:8080/engine-rest"
        )
        self.camunda_login = os.getenv("CAMUNDA_LOGIN", default=None)
        self.camunda_password = os.getenv("CAMUNDA_PASSWORD", default=None)
        self.executors = executors


cfg = Config()
