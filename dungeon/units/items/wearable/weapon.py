from dataclasses import dataclass

from dungeon.units.items.wearable.wearable_item import WearableItem


@dataclass
class Weapon(WearableItem):
    damage: int
    magic: int
