from abc import ABC, abstractmethod
from typing import List

import dungeon.tiles as Tiles


class MapGenerator(ABC):
    @abstractmethod
    def __init__(self, map_size_x, map_size_y):
        self.tiles = [[Tiles.Empty]*map_size_x for _ in range(map_size_y)]

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

    def get_tiles(self) -> List[List[Tiles.Tile]]:
        return self.tiles
