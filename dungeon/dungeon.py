from typing import List

from dungeon.tiles import Tile
from dungeon.units.unit import Unit


class Dungeon:
    # should have units (and be able to make them perform actions),
    # entities (items) and a tile map
    def __init__(self, map: List[List[Tile]], units: List[Unit]):
        # TODO: add units too
        self.map = map
        self.units = units
