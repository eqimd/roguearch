from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from dungeon.units.actions.action import Action
from dungeon.tiles import Tile
from dungeon.units.actions.action_result import ActionResult, Fail
from dungeon.units.entity import Entity


class Unit(Entity):
    def __init__(self, pos_x: int, pos_y: int) -> None:
        self.__x = pos_x
        self.__y = pos_y
        self.__action: Optional[Action] = None

        self.__hp: int = 0
        self.__mp: int = 0

    def set_action(self, action: Action) -> None:
        self.__action = action

    def perform_action(self) -> ActionResult:
        return self.__action.perform() if self.__action is not None else Fail('Action not set')

    def calculate_distance_self(self, other: Unit, units: List[Unit], tiles: List[List[Tile]]) -> int:
        return Unit.calculate_distance(self.x, self.y, other, units, tiles)

    @staticmethod
    def calculate_distance(pos_x: int, pos_y: int, other: Unit, units: List[Unit], tiles: List[List[Tile]]) -> int:
        start = (pos_x, pos_y)
        used = set(start)
        s_queue: List[Tuple[Tuple[int, int], int]] = [(start, 0)]
        t = (other.x, other.y)

        while s_queue:
            s_cur = s_queue.pop(0)
            if s_cur[0] == t:
                return s_cur[1]

            for x_diff in [-1, 0, 1]:
                for y_diff in [-1, 0, 1]:
                    next_step = (s_cur[0][0] + x_diff, s_cur[0][1] + y_diff)
                    if (
                            next_step[0] < 0 or next_step[0] >= len(tiles) or
                            next_step[1] < 0 or next_step[1] >= len(tiles[0]) or
                            tiles[next_step[0]][next_step[1]].colliding or
                            any((unit.x, unit.y) == next_step for unit in units) or
                            next_step in used
                    ):
                        continue

                    s_queue.append((next_step, s_cur[1] + 1))
                    used.add(next_step)

        # means there is no path (unlikely to happen)
        return -1

    def have_hp(self):
        return self.hp != 0

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def hp(self) -> int:
        return self.__hp

    @hp.setter
    def hp(self, value):
        self.__hp = value

    @property
    def mp(self) -> int:
        return self.__mp

    @mp.setter
    def mp(self, value):
        self.__mp = value

    @property
    @abstractmethod
    def max_hp(self) -> int:
        pass

    @property
    @abstractmethod
    def max_mp(self) -> int:
        pass

    @property
    @abstractmethod
    def hit_chance(self) -> float:
        pass

    @property
    @abstractmethod
    def crit_chance(self) -> float:
        pass

    @property
    @abstractmethod
    def physical_damage(self) -> int:
        pass

    @property
    @abstractmethod
    def magical_damage(self) -> int:
        pass

    @property
    @abstractmethod
    def dodge_chance(self) -> float:
        pass

    @property
    @abstractmethod
    def bleed_resistance(self) -> float:
        pass

    @property
    @abstractmethod
    def poison_resistance(self) -> float:
        pass

    @property
    @abstractmethod
    def debuff_resistance(self) -> float:
        pass
