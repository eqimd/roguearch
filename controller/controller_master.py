from controller.controller import Controller
from controller.controller_enum import ControllerEnum
from controller.controller_exit import ControllerExit
from meta.result import Result

from blessed import Terminal


class ControllerMaster:
    terminal: Terminal
    controller: Controller

    def __init__(self, terminal: Terminal, cont: Controller) -> None:
        ControllerMaster.terminal = terminal
        ControllerMaster.set_underlying_controller(cont)

    @classmethod
    def set_underlying_controller(cls, cont: Controller) -> None:
        cls.controller = cont
        cls.__flush_screen()

    @classmethod
    def forward_and_parse_on_not_ok(cls, key: str) -> Result:
        res = ControllerMaster.controller.parse_key(key)

        if not res.ok and res.msg == 'Invalid input':
            res = cls.__parse_key(key)

        return res

    @classmethod
    def __flush_screen(cls) -> None:
        print(cls.terminal.clear + cls.terminal.move_xy(0, cls.terminal.height - 1), end='')
        cls.controller.draw_screen()

    @classmethod
    def __parse_key(cls, key: str) -> Result:
        res = Result()

        match ControllerMaster.controller.id:
            case ControllerEnum.MainMenu:
                match key:
                    case 'KEY_ESCAPE':
                        cls.set_underlying_controller(ControllerExit())
                    case _:
                        res.fail('Invalid input')

        return res
