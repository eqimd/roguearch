from abc import abstractmethod
from dataclasses import dataclass

from dungeon.units.items.item_enum import ItemEnum


@dataclass
class Item:
    id: ItemEnum
    weight: float

    @property
    @abstractmethod
    def symbol(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass


class ItemOnScreen:
    def __init__(self, item: Item, x: int, y: int):
        self.item = item
        self.x = x
        self.y = y
