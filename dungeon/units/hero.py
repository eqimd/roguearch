from dataclasses import dataclass
from math import floor
from random import random
from typing import Any, List, cast

from dungeon.units.effects.effect import Effect
from dungeon.units.effects.effect_enum import EffectEnum
from dungeon.units.items.wearable.armor import Armor
from dungeon.units.items.wearable.trinket import Trinket
from dungeon.units.items.wearable.weapon import Weapon
from dungeon.units.unit import Unit


@dataclass
class HeroAttributes:
    vitality: int
    strength: int
    perseverance: int
    perception: int
    dexterity: int
    intelligence: int


class Hero(Unit):
    def __init__(self, attrs: HeroAttributes) -> None:
        self.base_max_hp = 40
        self.base_max_mp = 10
        self.base_attack = 4
        self.base_magic = 4
        self.base_accuracy = 0
        self.base_resistance = 0
        self.base_max_weight = 5

        self.attrs = attrs

        self.status_effects: List[Effect] = list()

        # give at start or load from file?
        self.weapon: Weapon
        self.upper_body: Armor
        self.lower_body: Armor
        self.ring: Trinket
        self.amulet: Trinket
        # WearableItem with effects - apply effects

    def cast_on_self(self) -> None:
        pass

    def cast_on_enemy(self) -> None:
        pass

    @property
    def max_hp(self) -> int:
        base = self.base_max_hp + 5 * self.attrs.vitality
        shifted = cast(int, self.__apply_effects(EffectEnum.HPOffset, base))
        multiplier = cast(float, self.__apply_effects(EffectEnum.HPMultiplier, 1))
        return floor(shifted * multiplier)

    @property
    def max_mp(self) -> int:
        base = self.base_max_hp + 2 * self.attrs.vitality
        shifted = cast(int, self.__apply_effects(EffectEnum.MPOffset, base))
        multiplier = cast(float, self.__apply_effects(EffectEnum.MPMultiplier, 1))
        return floor(shifted * multiplier)

    @property
    def accuracy(self) -> int:
        base = self.base_accuracy + self.attrs.perception
        shifted = cast(int, self.__apply_effects(EffectEnum.AccOffset, base))
        return shifted

    @staticmethod
    def hit_value_to_chance(value: int) -> float:
        return 1 / (1 + 4 ** (- 1 - value / 10))

    @property
    def hit_chance(self) -> float:
        return Hero.hit_value_to_chance(self.accuracy)

    @staticmethod
    def crit_value_to_chance(value: int) -> float:
        return 1 - 2 ** (- value / 20)

    @property
    def crit_chance(self) -> float:
        base_no_crit = 1 - Hero.crit_value_to_chance(self.accuracy)
        modifier_no_crit = cast(float, self.__apply_effects(EffectEnum.CritMultiplier, 1))
        return 1 - base_no_crit * modifier_no_crit

    @property
    def physical_damage(self) -> int:
        base = self.base_attack + self.attrs.strength
        return (2 * base) if random() < self.crit_chance else base

    @property
    def magical_damage(self) -> int:
        base = self.base_magic + self.attrs.intelligence
        return (2 * base) if random() < self.crit_chance else base

    @property
    def resistance(self) -> int:
        return self.base_resistance + self.attrs.perseverance

    @staticmethod
    def resistance_value_to_chance(value: int) -> float:
        return 1 - 2 ** (- value / 20)

    @property
    def bleed_resistance(self) -> float:
        modifier_no_resist = cast(float, self.__apply_effects(EffectEnum.BleedResMultiplier, 1))
        base_no_resist = 1 - Hero.resistance_value_to_chance(self.resistance)
        return 1 - base_no_resist * modifier_no_resist

    @property
    def poison_resistance(self) -> float:
        base_no_resist = 1 - Hero.resistance_value_to_chance(self.resistance)
        modifier_no_resist = cast(float, self.__apply_effects(EffectEnum.PoisonResMultiplier, 1))
        return 1 - base_no_resist * modifier_no_resist

    @property
    def debuff_resistance(self) -> float:
        base_no_resist = 1 - Hero.resistance_value_to_chance(self.resistance)
        modifier_no_resist = cast(float, self.__apply_effects(EffectEnum.DebuffResMultiplier, 1))
        return 1 - base_no_resist * modifier_no_resist

    def __apply_effects(self, effect_type: EffectEnum, *args: Any) -> Any:
        cur_args = args

        for effect in self.status_effects:
            cur_args = effect.apply_if_possible(effect_type, *cur_args)

        for effect in self.weapon.effects:
            cur_args = self.weapon.apply_effects(effect_type, *cur_args)

        for effect in self.upper_body.effects:
            cur_args = self.weapon.apply_effects(effect_type, *cur_args)

        for effect in self.lower_body.effects:
            cur_args = self.weapon.apply_effects(effect_type, *cur_args)

        for effect in self.ring.effects:
            cur_args = self.weapon.apply_effects(effect_type, *cur_args)

        for effect in self.amulet.effects:
            cur_args = self.weapon.apply_effects(effect_type, *cur_args)

        return cur_args
