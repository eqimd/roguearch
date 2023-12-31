from abc import ABC, abstractmethod

from controller.controller_enum import ControllerEnum
from meta.result import Result


class Controller(ABC):
    id: ControllerEnum

    @abstractmethod
    def draw_screen(self) -> None:
        "Calls underlying screen to be drawn from the controller state"

    @abstractmethod
    def parse_key(self, key: str) -> Result:
        "Exectues logic based on input key"
        pass
