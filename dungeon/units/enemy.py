from __future__ import annotations

from random import shuffle
from typing import List

from dungeon.units.hero import Hero
from dungeon.units.unit import Unit
from dungeon.tiles import Tile

import dungeon.units.actions as Actions


class Enemy(Unit):
    def __init__(
            self,
            pos_x: int,
            pos_y: int,
            max_hp: int,
            max_mp: int,
            hit_chance: float,
            crit_chance: float,
            physical_damage: int,
            magical_damage: int,
            dodge_chance: float,
            bleed_resistance: float,
            poison_resistance: float,
            debuff_resistance: float,
            hero_seen: bool = False,
    ) -> None:
        super().__init__(pos_x, pos_y)

        self.__max_hp = max_hp
        self.__max_mp = max_mp
        self.__hit_chance = hit_chance
        self.__crit_chance = crit_chance
        self.__physical_damage = physical_damage
        self.__magical_damage = magical_damage
        self.__dodge_chance = dodge_chance
        self.__bleed_resistance = bleed_resistance
        self.__poison_resistance = poison_resistance
        self.__debuff_resistance = debuff_resistance

        self.hp = self.__max_hp
        self.mp = self.__max_mp

        self.hero_seen = hero_seen

    @staticmethod
    def make_basic_enemy_by_level(pos_x: int, pos_y: int, level: int, hero_seen: bool = False) -> Enemy:
        return Enemy(pos_x, pos_y, 10 + 2 * level, 0, 0.8, 0.1, 2 + level, 0, 0.1, 0.2, 0.2, 0.2, hero_seen)

    def generate_action(self, hero: Hero, tiles: List[List[Tile]]) -> Actions.Action:
        """
        Primitive behaviour: attack if close
        to the hero, come closer if not
        """
        if not self.hero_seen:
            return Actions.LookForHeroAction(self, hero)

        if self.calculate_distance_self(hero, tiles) < 2:
            return Actions.AttackAction(self, hero)

        else:
            moves = [(x_diff, y_diff) for x_diff in [-1, 0, 1] for y_diff in [-1, 0, 1]]
            shuffle(moves)

            moves.sort(key=lambda move: self.calculate_distance(self.x + move[0], self.y + move[1], hero, tiles))
            return Actions.MoveAction(self, moves[0])

    @property
    def max_hp(self) -> int:
        return self.__max_hp

    @property
    def max_mp(self) -> int:
        return self.__max_mp

    @property
    def hit_chance(self) -> float:
        return self.__hit_chance

    @property
    def crit_chance(self) -> float:
        return self.__crit_chance

    @property
    def physical_damage(self) -> int:
        return self.__physical_damage

    @property
    def magical_damage(self) -> int:
        return self.__magical_damage

    @property
    def dodge_chance(self) -> float:
        return self.__dodge_chance

    @property
    def bleed_resistance(self) -> float:
        return self.__bleed_resistance

    @property
    def poison_resistance(self) -> float:
        return self.__poison_resistance

    @property
    def debuff_resistance(self) -> float:
        return self.__debuff_resistance
