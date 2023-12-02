
from abc import ABC, abstractmethod


class Entity(ABC):
    @property
    @abstractmethod
    def symbol(self) -> str:
        pass
