
from typing import Any

from blessed import Terminal
from screen.screen import Screen


class ScreenInventory(Screen):
    items_in_row = 6
    items_in_column = 3

    def __init__(self, terminal: Terminal, inventory) -> None:
        self.cursor_item_pos = (0, 0)
        self.terminal = terminal
        self.inventory = inventory
        

    def draw(self, *args: Any, **kwargs: Any) -> None:
        Screen.flush(self.terminal)

        width_offset = (self.terminal.width - 4*ScreenInventory.items_in_row + 1) // 2
        height_offset = (self.terminal.height - 4*ScreenInventory.items_in_column + 1) // 2

        with self.terminal.location(width_offset + 2*ScreenInventory.items_in_column + 2, height_offset - 2):
            print('Inventory', end='')

        for y in range(0, 2*ScreenInventory.items_in_column, 2):
            with self.terminal.location(width_offset, height_offset + y):
                for _ in range(2*ScreenInventory.items_in_row):
                    print('*–', end='')
                print('*', end='')

            with self.terminal.location(width_offset, height_offset + y + 1):
                for _ in range(2*ScreenInventory.items_in_row):
                    print('| ', end='')
                print('|', end='')

        y = 2*ScreenInventory.items_in_column
        with self.terminal.location(width_offset, height_offset + y):
            for _ in range(2*ScreenInventory.items_in_row):
                print('*–', end='')
            print('*', end='')


    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)