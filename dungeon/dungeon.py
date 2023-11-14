from typing import List

from dungeon.tiles import Tile


class Dungeon:
    def __init__(self, map: List[List[Tile]]):
        # TODO: add units too
        self.map = map
