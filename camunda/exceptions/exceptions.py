class BPMNException(Exception):
    def __init__(self, message):
        self.message = message


class CamundaComputeException(Exception):
    def __init__(self, message):
        self.message = message
