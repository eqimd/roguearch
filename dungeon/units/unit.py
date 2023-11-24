from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from dungeon.units.actions import Action
from dungeon.tiles import Tile
from meta.result import Result


class Unit(ABC):
    def __init__(self, pos_x: int, pos_y: int) -> None:
        self.x = pos_x
        self.y = pos_y
        self.action: Optional[Action] = None

        self.hp: int
        self.mp: int

    def set_action(self, action: Action) -> None:
        self.action = action

    def perform_action(self) -> Result:
        return self.action.perform() if self.action is not None else Result(ok=False, msg='Action not set')

    def calculate_distance_self(self, other: Unit, tiles: List[List[Tile]]) -> int:
        return Unit.calculate_distance(self.x, self.y, other, tiles)

    @staticmethod
    def calculate_distance(pos_x: int, pos_y: int, other: Unit, tiles: List[List[Tile]]) -> int:
        checked = set()
        s_queue: List[Tuple[Tuple[int, int], int]] = [((pos_x, pos_y), 0)]
        t = (other.x, other.y)

        while s_queue:
            s_cur = s_queue.pop()
            if s_cur[0] == t:
                return s_cur[1]

            checked.add(s_cur[0])
            for x_diff in [-1, 0, 1]:
                for y_diff in [-1, 0, 1]:
                    next_step = (s_cur[0][0] + x_diff, s_cur[0][1] + y_diff)
                    if tiles[next_step[0]][next_step[1]].colliding or next_step in checked:
                        continue

                    s_queue.append((next_step, s_cur[1] + 1))

        # means there is no path (unlikely to happen)
        return -1

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
