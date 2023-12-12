from abc import ABC, abstractmethod

from dungeon.units.actions.action_result import ActionResult


class BaseMob(ABC):

    @abstractmethod
    def perform_action(self) -> ActionResult:
        pass

    @property
    @abstractmethod
    def exp_points(self) -> int:
        pass
