from requests import request
from requests.auth import HTTPBasicAuth
import os
import sys

BASE_PATH = "workflows"
# docker compose
camunda_url = sys.argv[1]
camunda_login = sys.argv[2]
camunda_password = sys.argv[3]


class CamundaClient:
    def __init__(self, base_rest_url: str, login: str = "", password: str = ""):
        self._base_rest_url = base_rest_url
        self._login = login
        self._password = password

    def __call__camunda(self, method, url_path, **kwargs):
        print(f"{self._base_rest_url}{url_path}")
        r = request(
            method,
            f"{self._base_rest_url}{url_path}",
            **kwargs,
            verify=False,
            auth=HTTPBasicAuth(self._login, self._password),
        )
        print(r.text)
        r.raise_for_status()
        return r.json()

    def send_new_deployment(self, workflows, forms):
        files = {
            "deployment-source": "Camunda python client",
        }
        for workflow in workflows:
            form_name = workflow.split("/")[-1]
            files[form_name] = open(workflow, "rb")
        for form in forms:
            form_name = form.split("/")[-1]
            files[form_name] = open(form, "rb")
        print("Send next files:")
        print(files)
        self.__call__camunda(
            "post", "/deployment/create", files=files,
        )


camunda = CamundaClient(camunda_url, camunda_login, camunda_password)

for dir in os.listdir(BASE_PATH):
    PROCESS_PATH = os.path.join(BASE_PATH, dir)
    BPMN_FORMAT = "bpmn"
    bpmn_files = [
        os.path.join(PROCESS_PATH, fn)
        for fn in os.listdir(PROCESS_PATH)
        if fn.endswith(BPMN_FORMAT)
    ]
    HTML_FORMAT = "html"
    camunda_form_files = [
        os.path.join(PROCESS_PATH, fn)
        for fn in os.listdir(PROCESS_PATH)
        if fn.endswith(HTML_FORMAT)
    ]
    for subdir in os.listdir(PROCESS_PATH):
        SUBFOLDER_PROCESS_PATH = os.path.join(PROCESS_PATH, subdir)
        if os.path.isdir(SUBFOLDER_PROCESS_PATH):
            subfolder_bpmn_files = [
                os.path.join(SUBFOLDER_PROCESS_PATH, fn)
                for fn in os.listdir(SUBFOLDER_PROCESS_PATH)
                if fn.endswith(BPMN_FORMAT)
            ]
            bpmn_files.extend(subfolder_bpmn_files)

    print("found files")
    print(bpmn_files)
    print(camunda_form_files)
    try:
        camunda.send_new_deployment(bpmn_files, camunda_form_files)
    except Exception as ex:
        print(ex)
        raise ex
