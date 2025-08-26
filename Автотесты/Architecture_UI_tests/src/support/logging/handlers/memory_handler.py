import logging
from collections import deque


class MemoryErrorHandler(logging.Handler):
    def __init__(self, capacity=10):
        super().__init__()
        self.capacity = capacity
        self.records = deque(maxlen=capacity)

    def emit(self, record):
        if record.levelno >= logging.ERROR:
            msg = record.getMessage()

            self.records.append(msg)

    def get_errors(self):
        return list(self.records)
