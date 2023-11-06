from controller.controller import Controller
from controller.controller_enum import ControllerEnum
from meta.result import Result


# dummy controller to stop the game gracefully
class ControllerExit(Controller):
    id = ControllerEnum.Exit

    def __init__(self) -> None:
        pass

    def draw_screen(self) -> None:
        pass

    def parse_key(self, key: str) -> Result:
        return Result()
