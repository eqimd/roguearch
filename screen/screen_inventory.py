from ast import Invert
from typing import Tuple

from blessed import Terminal
from dungeon.inventory import Inventory
from screen.screen import Screen


class ScreenInventory(Screen):
    def __init__(self, terminal: Terminal, inventory: Inventory) -> None:
        self.terminal = terminal
        self.inventory = inventory
        

    def draw(self, chosen_item_pos: Tuple[int, int]) -> None:
        Screen.flush(self.terminal)

        self.__draw_inventory_title()
        self.__draw_inventory_skeleton()
        self.__draw_items()
        self.__draw_chosen_item_background(chosen_item_pos)

    def __draw_inventory_skeleton(self) -> None:
        width_offset = self.__get_width_offset()
        height_offset = self.__get_height_offset()

        for y in range(0, 2*Inventory.items_in_column, 2):
            with self.terminal.location(width_offset, height_offset + y):
                for _ in range(Inventory.items_in_row):
                    print('*–', end='')
                print('*', end='')

            with self.terminal.location(width_offset, height_offset + y + 1):
                for _ in range(Inventory.items_in_row):
                    print('| ', end='')
                print('|', end='')

        y = 2*Inventory.items_in_column
        with self.terminal.location(width_offset, height_offset + y):
            for _ in range(Inventory.items_in_row):
                print('*–', end='')
            print('*', end='')

    
    def __draw_items(self) -> None:
        # TODO: use items, not 'x' stubs
        width_offset = self.__get_width_offset()
        height_offset = self.__get_height_offset()

        for y in range(1, 2*Inventory.items_in_column, 2):
            for x in range(1, 2*Inventory.items_in_row, 2):
                with self.terminal.location(width_offset + x, height_offset + y):
                    print('x', end='')


    def __draw_chosen_item_background(self, chosen_item_pos: Tuple[int, int]) -> None:
        x, y = chosen_item_pos

        width_offset = self.__get_width_offset() + 2*x + 1
        height_offset = self.__get_height_offset() + 2*y + 1

        # TODO: use item, not 'x' stub
        with self.terminal.location(width_offset, height_offset):
            print(self.terminal.on_color_rgb(0, 150, 0) + 'x', end='')

    
    def __draw_inventory_title(self) -> None:
        width_offset = self.__get_width_offset()
        height_offset = self.__get_height_offset()

        with self.terminal.location(width_offset + Inventory.items_in_column - 1, height_offset - 2):
            print('Inventory', end='')


    def __get_width_offset(self) -> int:
        return (self.terminal.width - 2*Inventory.items_in_row + 1) // 2


    def __get_height_offset(self) -> int:
        return (self.terminal.height - 2*Inventory.items_in_column + 1) // 2


    def update(self) -> None:
        pass