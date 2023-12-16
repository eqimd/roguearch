from abc import ABC, abstractmethod
from typing import Optional, Tuple
from dungeon.dungeon import Dungeon

import dungeon.tiles as Tiles
from dungeon.units.hero import Hero
from dungeon.units.mobs.mob_factory import MobFactory


class DungeonGeneratorException(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message

    def __str__(self) -> str:
        if self.message:
            msg = f'Error occurred during map loading: {self.message}'
        else:
            msg = 'An error occurred during map loading'

        return msg


class DungeonGenerator(ABC):
    @abstractmethod
    def __init__(self, map_size_x: int, map_size_y: int, hero: Hero):
        self.dungeon = Dungeon(
            [[Tiles.Empty]*map_size_x for _ in range(map_size_y)],
            hero,
            list(),
            list()
        )

        self.start_point: Optional[Tuple[int, int]] = None
        self.end_point: Optional[Tuple[int, int]] = None

    @abstractmethod
    def make_floor(self) -> None:
        """Function dedicated to placing floor tiles"""
        pass

    @abstractmethod
    def make_doors(self) -> None:
        """Function dedicated to placing door tiles"""
        pass

    @abstractmethod
    def make_walls(self) -> None:
        """Function dedicated to placing wall tiles"""
        pass

    @abstractmethod
    def make_start_exit_positions(self) -> None:
        """Function dedicated to placing wall tiles"""
        pass

    @abstractmethod
    def make_exit(self) -> None:
        """Function dedicated to placing mobs on the map"""
        pass

    @abstractmethod
    def place_mobs(self, mob_factory: MobFactory, level: int) -> None:
        """Function dedicated to placing mobs on the map"""
        pass

    def get_dungeon(self):
        return self.dungeon
