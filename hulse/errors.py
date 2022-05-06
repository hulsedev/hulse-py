from typing import Any


class UnsupportedTaskError(Exception):
    def __init__(self, task: str, expression: Any = None):
        self.message = f"The task provided ({task}) is not supported."
        self.expression = expression


class UnsufficientResources(Exception):
    def __init__(self, expression: Any = None):
        self.message = f"No running cluster resource was found."
        self.expression = expression


class HulseError(Exception):
    def __init__(self, status: int = None, expression: Any = None):
        self.message = f"Received error code {status}."
        self.expression = expression
