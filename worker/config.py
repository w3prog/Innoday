import os

from worker.executors import (
    load_data_executor,
    check_completeness_executor,
    check_validity_executor,
    check_uniqueness_executor,
    check_consistency_executor,
    check_timeliness_executor,
    generate_quality_report_executor,
    convert_timeseries_executor,
    generate_report_executor,
    store_data_executor
)

executors = {
    "load_data": load_data_executor,
    "check_completeness": check_completeness_executor,
    "check_validity": check_validity_executor,
    "check_uniqueness": check_uniqueness_executor,
    "check_consistency": check_consistency_executor,
    "check_timeliness": check_timeliness_executor,
    "generate_quality_report": generate_quality_report_executor,
    "convert_data": convert_timeseries_executor,
    "generate_report": generate_report_executor,
    "store_data": store_data_executor,
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
