from dataclasses import dataclass

from dungeon.units.items.wearable.wearable_item import WearableItem


@dataclass
class Trinket(WearableItem):

    @property
    def symbol(self) -> str:
        return "!"

    @property
    def description(self) -> str:
        return "Trinket"

