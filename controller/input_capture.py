from blessed import Terminal

from controller.controller_enum import ControllerEnum
from controller.controller_master import ControllerMaster


class InputCapture:
    terminal: Terminal
    master_controller: ControllerMaster

    def __init__(self, terminal: Terminal, master_controller: ControllerMaster) -> None:
        InputCapture.terminal = terminal
        InputCapture.master_controller = master_controller

    def await_and_forward_input(self) -> None:
        with InputCapture.terminal.cbreak():
            while InputCapture.master_controller.controller.id != ControllerEnum.Exit:
                stroke = InputCapture.terminal.inkey()
                key: str = stroke.name if stroke.name is not None else str(stroke).lower()
                if key:
                    InputCapture.master_controller.forward_and_parse_on_not_ok(key)
