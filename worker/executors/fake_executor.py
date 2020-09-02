import time
import random


def fake_executor(task):
    return {"results": {"value": "SUCCESS"}}


def fake_executor_random(task):
    time.sleep(random.randint(5, 10))
    return {"results": {"value": "SUCCESS"}}
