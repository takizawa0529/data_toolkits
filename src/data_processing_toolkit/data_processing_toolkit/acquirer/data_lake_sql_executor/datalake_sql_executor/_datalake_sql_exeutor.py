from abc import ABC, abstractmethod

class DatalakeSqlExecutor(ABC):
    def __init__(self):
        self._create_connection()

    @abstractmethod
    def _create_connection(self):
        pass

    @abstractmethod
    def fetch(self):
        pass