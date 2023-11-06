from blessed import Terminal

from controller.controller import Controller
from controller.controller_enum import ControllerEnum
from meta.result import Result
from screen.screen_main_menu import ScreenMainMenu


class ControllerMainMenu(Controller):
    id = ControllerEnum.MainMenu

    menu_items = [
        'Start Game',
        'Load Game'
    ]

    def __init__(self, terminal: Terminal) -> None:
        super().__init__()
        self.screen = ScreenMainMenu(terminal)
        self.selection = 0

    def draw_screen(self) -> None:
        self.screen.draw(self.selection)

    def parse_key(self, key: str) -> Result:
        res = Result()

        match key:
            case "w" | "KEY_UP":
                new_selection = (self.selection - 1) % len(self.menu_items)
                self.screen.update(new_selection, self.selection)
                self.selection = new_selection
            case "s" | "KEY_DOWN":
                new_selection = (self.selection + 1) % len(self.menu_items)
                self.screen.update(new_selection, self.selection)
                self.selection = new_selection
            case "q" | "KEY_ENTER":
                match self.selection:
                    case 0:
                        # TODO: start the game
                        pass
                    case 1:
                        # TODO: load the game
                        pass
            case _:
                res.fail("Invalid input")

        return res
