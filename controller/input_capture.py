from blessed import Terminal

from controller.controller_enum import ControllerEnum
from controller.controller_master import ControllerMaster


class InputCapture:
    terminal: Terminal
    controller_master: ControllerMaster

    def __init__(self, terminal: Terminal, controller_master: ControllerMaster) -> None:
        InputCapture.terminal = terminal
        InputCapture.controller_master = controller_master

    def await_and_forward_input(self) -> None:
        with InputCapture.terminal.cbreak():
            while InputCapture.controller_master.controller.id != ControllerEnum.Exit:
                stroke = InputCapture.terminal.inkey()
                key: str = stroke.name if stroke.name is not None else str(stroke).lower()
                if key:
                    InputCapture.controller_master.forward_and_parse_on_not_ok(key)
