from abc import ABC, abstractmethod
from dungeon.units.actions.action_result import ActionResult


class Action(ABC):
    @abstractmethod
    def perform(self) -> ActionResult:
        """
        Called by a unit from its action field
        Yields whether the action succeeded
        """
        pass
