from typing import Any
from blessed import Terminal

from screen.screen import Screen
from dungeon.dungeon import Dungeon

class ScreenDungeon(Screen):
    def __init__(self, terminal: Terminal, dungeon: Dungeon):
        self.terminal = terminal
        self.dungeon = dungeon

    def draw(self, *args: Any, **kwargs: Any) -> None:
        self.__flush_screen()

        width_offset = (self.terminal.width - len(self.dungeon.map)) // 2 - 1
        height_offset = (self.terminal.height - len(self.dungeon.map[0])) // 2 + 1

        for idx, row in enumerate(self.dungeon.map):
            for idy, tile in enumerate(row):
                with self.terminal.location(width_offset + idx, height_offset + idy):
                    print(tile, end = '')

        for unit in self.dungeon.units:
            with self.terminal.location(width_offset + unit.x, height_offset + unit.y):
                print(unit.symbol, end='')

    def __flush_screen(self) -> None:
        print(self.terminal.clear + self.terminal.move_xy(0, self.terminal.height - 1), end='')
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def draw_msg(self, msg: str) -> None:
        with self.terminal.location(10, self.terminal.height - 10):
            print(msg, end='')