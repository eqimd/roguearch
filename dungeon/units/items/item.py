from dataclasses import dataclass

from dungeon.units.items.item_enum import ItemEnum


@dataclass
class Item:
    id: ItemEnum
    weight: float
