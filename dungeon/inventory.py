
from typing import List
from dungeon.units.items.item import Item


class Inventory():
    def __init__(self, items: List[Item]):
        self.items = items