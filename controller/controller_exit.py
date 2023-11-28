from controller.controller import Controller
from controller.controller_enum import ControllerEnum
from meta.result import Result, Ok


# dummy controller to stop the game gracefully
class ControllerExit(Controller):
    id = ControllerEnum.Exit

    def __init__(self) -> None:
        pass

    def draw_screen(self) -> None:
        pass

    def prev_controller(self) -> Controller:
        return self

    def parse_key(self, key: str) -> Result:
        return Ok('')
