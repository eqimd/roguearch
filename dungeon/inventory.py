from typing import List
from dungeon.units.items.item import Item


class Inventory():
    items_in_row = 6
    items_in_column = 3

    def __init__(self, items: List[Item]):
        self.items = items

    def add_item(self, item: Item) -> bool:
        if len(self.items) < Inventory.items_in_column * Inventory.items_in_row:
            self.items.append(item)
            
            return True
        else:
            return False