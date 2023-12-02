from dataclasses import dataclass
from math import floor
from typing import Any, List, cast, Optional
from dungeon.inventory import Inventory

from dungeon.units.effects.effect import Effect
from dungeon.units.effects.effect_enum import EffectEnum
from dungeon.units.items.item import Item
from dungeon.units.items.item_enum import ItemEnum
from dungeon.units.items.wearable.armor import Armor
from dungeon.units.items.wearable.trinket import Trinket
from dungeon.units.items.wearable.weapon import Weapon, WeaponFinka
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
    symbol_self = '@'

    def __init__(self, pos_x: int, pos_y: int, attrs: HeroAttributes, inventory: Inventory) -> None:
        super().__init__(pos_x, pos_y)

        self.base_max_hp = 40
        self.base_max_mp = 10
        self.base_attack = 4
        self.base_magic = 4
        self.base_accuracy = 0
        self.base_dodge = 0
        self.base_resistance = 0
        self.base_max_weight = 5

        self.hp = self.base_max_hp
        self.mp = self.base_max_mp

        # should be returned from the hero creation function
        self.attrs = attrs

        self.status_effects: List[Effect] = list()

        # give at start or load from file?
        # TODO: consider item attributes in calculation (and add attribute effects on items)
        # self.weapon = Weapon(ItemEnum.Weapon, 0, list(), 0, 0)

        self.weapon: Weapon = WeaponFinka()
        self.armor = Armor(ItemEnum.UpperBody, 0, list(), 0, 0)
        self.amulet = Trinket(ItemEnum.Amulet, 0, list())

        # later add:
        # Inventory
        # TODO: it is stub currently
        self.inventory = inventory

    def swap_item(self, item: Item) -> Optional[Item]:
        if isinstance(item, Weapon):
            old_weapon = self.weapon
            self.weapon = item
            return old_weapon
        
        # TODO: return none?
        return None

    @property
    def symbol(self) -> str:
        return Hero.symbol_self

    @property
    def max_hp(self) -> int:
        base = self.base_max_hp + 5 * self.attrs.vitality
        shifted = cast(int, self.__apply_effects(EffectEnum.HPOffset, base))
        multiplier = cast(float, self.__apply_effects(EffectEnum.HPMultiplier, 1))
        return floor(shifted * multiplier)

    @property
    def max_mp(self) -> int:
        base = self.base_max_hp + 2 * self.attrs.intelligence
        shifted = cast(int, self.__apply_effects(EffectEnum.MPOffset, base))
        multiplier = cast(float, self.__apply_effects(EffectEnum.MPMultiplier, 1))
        return floor(shifted * multiplier)

    @property
    def hit_chance(self) -> float:
        return Hero.__hit_value_to_chance(self.__accuracy)

    @property
    def crit_chance(self) -> float:
        base_no_crit = 1 - Hero.__crit_value_to_chance(self.__accuracy)
        modifier_no_crit = cast(float, self.__apply_effects(EffectEnum.CritMultiplier, 1))
        return 1 - base_no_crit * modifier_no_crit

    @property
    def physical_damage(self) -> int:
        return self.base_attack + self.attrs.strength

    # currently unused
    @property
    def magical_damage(self) -> int:
        return self.base_magic + self.attrs.intelligence

    @property
    def dodge_chance(self) -> float:
        base_no_dodge = 1 - Hero.__dodge_value_to_chance(self.__dodge)
        modifier_no_dodge = cast(float, self.__apply_effects(EffectEnum.DodgeMultiplier, 1))
        return 1 - base_no_dodge * modifier_no_dodge

    # currently unused
    @property
    def bleed_resistance(self) -> float:
        modifier_no_resist = cast(float, self.__apply_effects(EffectEnum.BleedResMultiplier, 1))
        base_no_resist = 1 - Hero.__resistance_value_to_chance(self.__resistance)
        return 1 - base_no_resist * modifier_no_resist

    # currently unused
    @property
    def poison_resistance(self) -> float:
        base_no_resist = 1 - Hero.__resistance_value_to_chance(self.__resistance)
        modifier_no_resist = cast(float, self.__apply_effects(EffectEnum.PoisonResMultiplier, 1))
        return 1 - base_no_resist * modifier_no_resist

    # currently unused
    @property
    def debuff_resistance(self) -> float:
        base_no_resist = 1 - Hero.__resistance_value_to_chance(self.__resistance)
        modifier_no_resist = cast(float, self.__apply_effects(EffectEnum.DebuffResMultiplier, 1))
        return 1 - base_no_resist * modifier_no_resist

    @property
    def __accuracy(self) -> int:
        base = self.base_accuracy + self.attrs.perception
        shifted = cast(int, self.__apply_effects(EffectEnum.AccOffset, base))
        return shifted

    @property
    def __dodge(self) -> int:
        return self.base_dodge + self.attrs.dexterity

    @property
    def __resistance(self) -> int:
        return self.base_resistance + self.attrs.perseverance

    @staticmethod
    def __hit_value_to_chance(value: int) -> float:
        return 1 / (1 + 4 ** (- 1 - value / 10))

    @staticmethod
    def __crit_value_to_chance(value: int) -> float:
        return max(1 - 2 ** (- value / 20), 0)

    @staticmethod
    def __dodge_value_to_chance(value: int) -> float:
        return max(1 - 2 ** (- value / 20), 0)

    @staticmethod
    def __resistance_value_to_chance(value: int) -> float:
        return max(0, 1 - 2 ** (- value / 20))

    def __apply_effects(self, effect_type: EffectEnum, *args: Any) -> Any:
        cur_args = args

        for effect in self.status_effects:
            cur_args = effect.apply_if_possible(effect_type, *cur_args)

        for effect in self.weapon.effects:
            cur_args = self.weapon.apply_effects(effect_type, *cur_args)

        for effect in self.armor.effects:
            cur_args = self.weapon.apply_effects(effect_type, *cur_args)

        for effect in self.amulet.effects:
            cur_args = self.weapon.apply_effects(effect_type, *cur_args)

        return cur_args
