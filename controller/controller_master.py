from controller.controller import Controller
from controller.controller_dungeon import ControllerDungeon
from controller.controller_enum import ControllerEnum
from controller.controller_exit import ControllerExit
from controller.controller_main_menu import ControllerMainMenu
from dungeon.dungeon_loader import DungeonLoader
from meta.result import *

from blessed import Terminal


class ControllerMaster:
    terminal: Terminal
    controller: Controller

    def __init__(self, terminal: Terminal) -> None:
        ControllerMaster.terminal = terminal
        ControllerMaster.controller = ControllerExit()

    @classmethod
    def set_underlying_controller(cls, cont: Controller) -> None:
        cls.controller = cont
        cls.__flush_screen()

    @classmethod
    def set_controller_main_menu(cls) -> None:
        cls.set_underlying_controller(ControllerMainMenu(cls.terminal, cls.controller))

    @classmethod
    def set_controller_exit(cls) -> None:
        cls.set_underlying_controller(ControllerExit())

    @classmethod
    def forward_and_parse_on_not_ok(cls, key: str) -> Result:
        res = ControllerMaster.controller.parse_key(key)

        match res:
            case Ok():
                return res
            case Fail():
                cls.set_controller_exit()
            case ForwardInput():
                cls.__parse_key(key)
            case ChangeToNextController():
                cls.set_underlying_controller(cls.controller.next_controller())
            case ChangeToPrevController():
                cls.set_underlying_controller(cls.controller.prev_controller())

        return res

    @classmethod
    def __flush_screen(cls) -> None:
        print(cls.terminal.clear + cls.terminal.move_xy(0, cls.terminal.height - 1), end='')
        cls.controller.draw_screen()

    @classmethod
    def __parse_key(cls, key: str) -> Result:
        match key:
            case "q" | "KEY_ESCAPE":
                cls.set_controller_exit()

        return Ok("")
