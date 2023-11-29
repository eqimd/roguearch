from typing import List
from dungeon.units.items.item import Item


class Inventory():
    items_in_row = 6
    items_in_column = 3

    def __init__(self, items: List[List[Item]]):
        self.items = items