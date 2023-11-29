from controller.controller_dungeon import ControllerDungeon
from dungeon.dungeon_loader import DungeonLoader
from meta.result import *

from blessed import Terminal

from controller.controller import Controller
from controller.controller_enum import ControllerEnum
from screen.screen_main_menu import ScreenMainMenu


class ControllerMainMenu(Controller):
    id = ControllerEnum.MainMenu

    def __init__(self, terminal: Terminal, prev_controller: Controller) -> None:
        super().__init__()
        self.prev_ctrl = prev_controller
        self.next_ctrl = self
        self.terminal = terminal
        self.screen = ScreenMainMenu(terminal)
        self.selection = 0

    def draw_screen(self) -> None:
        self.screen.draw(self.selection)

    def prev_controller(self) -> Controller:
        return self.prev_ctrl

    def next_controller(self) -> Controller:
        return self.next_ctrl

    def parse_key(self, key: str) -> Result:
        match key:
            case "w" | "KEY_UP":
                new_selection = (self.selection - 1) % len(self.screen.menu_items)
                self.screen.update(new_selection, self.selection)
                self.selection = new_selection

                return Ok("")
            case "s" | "KEY_DOWN":
                new_selection = (self.selection + 1) % len(self.screen.menu_items)
                self.screen.update(new_selection, self.selection)
                self.selection = new_selection

                return Ok("")
            case "KEY_ENTER":
                match self.selection:
                    case 0:
                        # TODO: start the game
                        return Fail("Not implemented")
                    case 1:
                        dungeon = DungeonLoader.load('./assets/basic_map.json')
                        self.next_ctrl = ControllerDungeon(self.terminal, dungeon, self)
                        
                        return ChangeToNextController()
                    case _:
                        return Fail("Unexpected") # should be never reached
            case _:
                return ForwardInput()
