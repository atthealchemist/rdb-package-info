from abc import ABCMeta, abstractmethod
from typing import List


class BaseCommand(metaclass=ABCMeta):
    """
    Base command class.
    """

    @abstractmethod
    def process(self, args: List[str]) -> None:
        """
        Method that performs command.
        Should be overrided in subclasses.
        """
        pass
