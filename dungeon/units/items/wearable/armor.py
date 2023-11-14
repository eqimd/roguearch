from dataclasses import dataclass
from typing import List

from dungeon.units.effects.effect import Effect
from dungeon.units.items.wearable.wearable_item import WearableItem


@dataclass
class Armor(WearableItem):
    armor: int
    firmness: int
    effects: List[Effect]
