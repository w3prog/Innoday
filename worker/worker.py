from camunda import ServiceWorker
import logging
from worker.config import cfg


def run_worker():
    if cfg.camunda_url:
        logging.info("Connecting to Camunda")
        camunda_external_tasks_worker = ServiceWorker(
            base_rest_url=cfg.camunda_url,
            executors=cfg.executors,
            login=cfg.camunda_login,
            password=cfg.camunda_password,
        )
        camunda_external_tasks_worker.subscribe()
    else:
        logging.error("Don't get CAMUNDA_URL")
