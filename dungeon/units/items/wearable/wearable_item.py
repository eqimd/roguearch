from dataclasses import dataclass
from typing import Any, List

from dungeon.units.items.item import Item
from dungeon.units.effects.effect_enum import EffectEnum
from dungeon.units.effects.effect import Effect


@dataclass
class WearableItem(Item):
    effects: List[Effect]

    def apply_effects(self, other_id: EffectEnum, *args: Any) -> Any:
        cur_args = args

        for effect in self.effects:
            cur_args = effect.apply_if_possible(other_id, *cur_args)

        return cur_args
