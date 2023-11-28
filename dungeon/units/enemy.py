from __future__ import annotations

from random import shuffle
from typing import List, Optional, Tuple

from dungeon.tiles import Tile
from dungeon.units.actions.action import Action
from dungeon.units.hero import Hero
from dungeon.units.unit import Unit

import dungeon.units.actions.actions as Actions


class Enemy(Unit):
    symbol_seen = 'o'
    symbol_not_seen = 'z'

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

    @property
    def symbol(self) -> str:
        return Enemy.symbol_seen if self.hero_seen else Enemy.symbol_not_seen

    def generate_action(self, hero: Hero, units: List[Unit], tiles: List[List[Tile]]) -> Optional[Action]:
        """
        Primitive behaviour: attack if close
        to the hero, come closer if not
        """
        if not self.hero_seen:
            found = self.__look_for_hero(hero, tiles)

            # enemy was not distrubed, continue the same action
            if not found:
                return self.action

        if self.calculate_distance_self(hero, units, tiles) < 2:
            return Actions.AttackAction(self, hero)

        else:
            moves = [(x_diff, y_diff) for x_diff in [-1, 0, 1] for y_diff in [-1, 0, 1]]
            shuffle(moves)

            moves.sort(key=lambda move: self.calculate_distance(self.x + move[0], self.y + move[1], hero, units, tiles))
            return Actions.MoveAction(self, moves[0], units, tiles)

    def __look_for_hero(self, hero: Hero, tiles: List[List[Tile]]) -> bool:
        # use obscuring to find out whether source can see target
        points = [(hero.x, hero.y)]

        up = hero.x < self.x
        down = hero.x > self.x
        left = hero.y < self.y
        right = hero.y > self.y

        if up:
            points.append((hero.x - 1, hero.y))
        if down:
            points.append((hero.x + 1, hero.y))
        if left:
            points.append((hero.x, hero.y - 1))
        if right:
            points.append((hero.x, hero.y + 1))

        if up and left:
            points.append((hero.x - 1, hero.y - 1))
        if down and left:
            points.append((hero.x + 1, hero.y - 1))
        if up and right:
            points.append((hero.x - 1, hero.y + 1))
        if down and right:
            points.append((hero.x + 1, hero.y + 1))

        for point in points:
            if not tiles[point[0]][point[1]].obscuring and any([
                tiles[x][y].obscuring
                for x, y
                in Enemy.__make_direct_path((self.x, self.y), point)
            ]):
                continue

            self.hero_seen = True
            return True

        return False

    @staticmethod
    def __make_direct_path(s: Tuple[int, int], t: Tuple[int, int]) -> List[Tuple[int, int]]:
        # definitely need tests for this function
        diff_x = t[0] - s[0]
        diff_y = t[1] - s[1]
        path: List[Tuple[int, int]] = list()

        diff_x_start, diff_x_end = min(diff_x, 0), max(0, diff_x)
        diff_y_start, diff_y_end = min(diff_y, 0), max(0, diff_y)

        if abs(diff_x) >= abs(diff_y):
            for diff_x_cur in range(diff_x_start, diff_x_end + 1):
                diff_y_frac: float = (
                    (diff_x_cur - diff_x_start) / (diff_x_end - diff_x_start) * (diff_y_end - diff_y_start)
                    + diff_y_start
                )
                path.append((s[0] + diff_x_cur, s[1] + round(diff_y_frac)))
        else:
            for diff_y_cur in range(diff_y_start, diff_y_end + 1):
                diff_x_frac: float = (
                    (diff_y_cur - diff_y_start) / (diff_y_end - diff_y_start) * (diff_x_end - diff_x_start)
                    + diff_x_start
                )
                path.append((s[0] + round(diff_x_frac), s[1] + diff_y_cur))

        return path

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
