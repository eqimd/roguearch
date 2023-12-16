from typing import List, Optional

from dungeon.tiles import Tile
from dungeon.units.hero import Hero
from dungeon.units.items.item import ItemOnScreen
from dungeon.units.unit import Unit


class Dungeon:
    # should have units (and be able to make them perform actions),
    # entities (items) and a tile map
    def __init__(self, map: List[List[Tile]], items: List[ItemOnScreen], hero: Hero, units: List[Unit]):
        self.map = map
        self.items = items
        self.hero = hero
        self.units = units
