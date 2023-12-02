from typing import Tuple
from blessed import Terminal
from controller.controller import Controller
from controller.controller_enum import ControllerEnum
from dungeon.inventory import Inventory
from dungeon.units.hero import Hero
from meta.result import ChangeToPrevController, Ok, Result

from screen.screen_inventory import ScreenInventory


class ControllerInventory(Controller):
    id = ControllerEnum.Inventory

    def __init__(self, terminal: Terminal, hero: Hero, prev_controller: Controller):
        self.screen = ScreenInventory(terminal, hero)
        self.terminal = terminal
        self.hero = hero
        self.inventory = hero.inventory
        self.prev_ctrl = prev_controller

        self.chosen_item_pos = (0, 0)

    def draw_screen(self) -> None:
        self.screen.draw(self.chosen_item_pos)
    
    def parse_key(self, key: str) -> Result:
        match key:
            case 'e' | 'q' | 'KEY_ESCAPE':
                return ChangeToPrevController()

            case 'd':
                # TODO: bound check

                x, _ = self.chosen_item_pos
                if x+1 < Inventory.items_in_row:
                    self.__update_chosen_item_pos((1, 0))
                    self.draw_screen()

            case 'w':
                # TODO: bound check

                _, y = self.chosen_item_pos
                if y > 0:
                    self.__update_chosen_item_pos((0, -1))
                    self.draw_screen()
            case 's':
                # TODO: bound check

                _, y = self.chosen_item_pos
                if y+1 < Inventory.items_in_column:
                    self.__update_chosen_item_pos((0, 1))
                    self.draw_screen()
            case 'a':
                # TODO: bound check

                x, _ = self.chosen_item_pos
                if x > 0:
                    self.__update_chosen_item_pos((-1, 0))
                    self.draw_screen()
            case 'f':
                x, y = self.chosen_item_pos
                item_pos = y*Inventory.items_in_row + x

                if item_pos >= len(self.inventory.items):
                    return Ok('')

                item = self.inventory.items[item_pos]

                # TODO: if none?
                old_item = self.hero.swap_item(item)
                if old_item is not None:
                    self.inventory.items[item_pos] = old_item

                self.draw_screen()

        return Ok('')
    

    def __update_chosen_item_pos(self, move_to: Tuple[int, int]) -> None:
        x0, y0 = self.chosen_item_pos
        x, y = move_to

        x0 += x
        y0 += y

        self.chosen_item_pos = (x0, y0)

    
    def prev_controller(self) -> Controller:
        return self.prev_ctrl
    
    def next_controller(self) -> Controller:
        return self