from abc import ABC, abstractmethod
from typing import Self

from controller.controller_enum import ControllerEnum
from meta.result import Result


class Controller(ABC):
    id: ControllerEnum

    @abstractmethod
    def draw_screen(self) -> None:
        "Calls underlying screen to be drawn from the controller state"

    @abstractmethod
    def parse_key(self, key: str) -> Result:
        "Executes logic based on input key"
        pass

    @abstractmethod
    def prev_controller(self) -> Self:
        "Returns previos controller"
        pass

    @abstractmethod
    def next_controller(self) -> Self:
        "Returns next controller to set"
        pass
