from typing import List, Optional

from dungeon.tiles import Tile
# from dungeon.units.hero import Hero
from dungeon.units.items.item import ItemOnScreen
# from dungeon.units.mobs.mob import Mob


class Dungeon:
    # should have units (and be able to make them perform actions),
    # entities (items) and a tile map
    def __init__(self, tiles: List[List[Tile]], hero, units, items: List[ItemOnScreen]):
        self.tiles = tiles
        self.hero = hero
        self.units = units
        self.items = items
