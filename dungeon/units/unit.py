from abc import ABC

from dungeon.units.actions.action import Action
from meta.result import Result


class Unit(ABC):
    action: Action

    def perform_action(self) -> Result:
        return self.action.perform()
