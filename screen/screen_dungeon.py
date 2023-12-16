from typing import Any
from blessed import Terminal

from screen.screen import Screen
from dungeon.dungeon import Dungeon

class ScreenDungeon(Screen):
    def __init__(self, terminal: Terminal, dungeon: Dungeon):
        self.terminal = terminal
        self.dungeon = dungeon

    def draw(self, *args: Any, **kwargs: Any) -> None:
        Screen.flush(self.terminal)

        self.__draw_map()
        self.__draw_items()
        self.__draw_units()
        self.__draw_hero()
        self.__draw_hero_stats()

    def __draw_map(self) -> None:
        width_offset = self.__get_width_offset()
        height_offset = self.__get_height_offset()

        for idx, row in enumerate(self.dungeon.tiles):
            for idy, tile in enumerate(row):
                with self.terminal.location(width_offset + idx, height_offset + idy):
                    print(tile, end = '')

    def __draw_items(self) -> None:
        width_offset = self.__get_width_offset()
        height_offset = self.__get_height_offset()

        for item in self.dungeon.items:
            with self.terminal.location(width_offset + item.x, height_offset + item.y):
                print(item.item.symbol, end='')

    def __draw_units(self) -> None:
        width_offset = self.__get_width_offset()
        height_offset = self.__get_height_offset()

        for unit in self.dungeon.units:
            with self.terminal.location(width_offset + unit.x, height_offset + unit.y):
                print(unit.symbol, end='')

    def __draw_hero(self) -> None:
        width_offset = self.__get_width_offset()
        height_offset = self.__get_height_offset()

        hero = self.dungeon.hero

        with self.terminal.location(width_offset + hero.x, height_offset + hero.y):
            print(hero.symbol, end='')

    def __draw_hero_stats(self) -> None:
        with self.terminal.location(self.terminal.width - 30, self.__get_height_offset()):
            print(f'Damage level: {self.dungeon.hero.weapon.damage}', end='\n')
        with self.terminal.location(self.terminal.width - 30, self.__get_height_offset() + 1):
            print(f'Dodge chance: {self.dungeon.hero.dodge_chance}', end='\n')
        with self.terminal.location(self.terminal.width - 30, self.__get_height_offset() + 2):
            print(f'Health: {self.dungeon.hero.hp}', end='\n')
        with self.terminal.location(self.terminal.width - 30, self.__get_height_offset() + 3):
            print(f'Level: {self.dungeon.hero.level}', end='\n')

    def __get_width_offset(self) -> int:
        return (self.terminal.width - len(self.dungeon.tiles)) // 2

    def __get_height_offset(self) -> int:
        return (self.terminal.height - len(self.dungeon.tiles[0])) // 2

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def draw_msg(self, msg: str) -> None:
        with self.terminal.location(10, self.terminal.height - 10):
            print(msg, end='')