from abc import ABC, abstractmethod

class BaseDataFactory(ABC):
    def get_data(self, **kwargs):
        data_acquirer = self._create_acquirer(**kwargs)
        return data_acquirer.acquire()

    @abstractmethod
    def _create_acquirer(self, **kwargs):
        pass


class BaseAcquirer(ABC):
    @abstractmethod
    def acquire(self):
        pass