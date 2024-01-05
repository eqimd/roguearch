from typing import List

from dungeon.tiles import Tile, Floor
from dungeon.units.items.item import ItemOnScreen
from dungeon.units.unit import Unit


class Dungeon:
    # should have units (and be able to make them perform actions),
    # entities (items) and a tile map
    def __init__(self, tiles: List[List[Tile]], hero, units: List[Unit], items: List[ItemOnScreen]):
        self.tiles = tiles
        self.hero = hero
        self.units = units
        self.items = items

    # method that verifies that a cell is a free floor cell
    def is_empty_floor_tile(self, x, y) -> bool:
        if x < 0 or y < 0 or x >= len(self.tiles) or y >= len(self.tiles[0]):
            return False
        if self.tiles[x][y] is not Floor:
            return False
        return len(list(filter(lambda unit: unit.x == x and unit.y == y, self.units))) == 0
