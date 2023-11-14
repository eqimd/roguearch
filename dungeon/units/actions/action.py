from abc import ABC, abstractmethod

from meta.result import Result


class Action(ABC):
    @abstractmethod
    def perform(self) -> Result:
        """
        Called by a unit from its action field
        Yields whether the action succeeded
        """
        pass
