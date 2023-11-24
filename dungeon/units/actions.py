from abc import ABC, abstractmethod
from random import random, randint
from typing import List, Tuple

from dungeon.tiles import Tile
from dungeon.units.enemy import Enemy
from dungeon.units.hero import Hero
from dungeon.units.unit import Unit
from meta.result import Result

# later add:
# UseItem
# MagicAction (?)
# ...


class Action(ABC):
    @abstractmethod
    def perform(self, *args, **kwargs) -> Result:  # type: ignore
        """
        Called by a unit from its action field
        Yields whether the action succeeded
        """
        pass


class AttackAction(Action):
    def __init__(self, source: Unit, target: Unit) -> None:
        self.source = source
        self.target = target

    def perform(self, randomness: float = 0.1) -> Result:
        # TODO: consider armor
        base_damage = (
            (2 * self.source.physical_damage)
            if random() < self.source.crit_chance
            else self.source.physical_damage
        )

        if random() > self.source.hit_chance:
            return Result(ok=False, msg='Attack missed')

        if random() > self.target.dodge_chance:
            return Result(ok=False, msg='Attack dodged')

        actual_damage = randint(round((1 - randomness) * base_damage), round((1 + randomness) * base_damage))

        self.target.hp = max(self.target.hp - actual_damage, 0)
        return Result()


class MoveAction(Action):
    def __init__(self, source: Unit, move: Tuple[int, int]) -> None:
        self.source = source
        self.move = move

    def perform(self, units: List[Unit], tiles: List[List[Tile]]) -> Result:
        next_pos = (self.source.x + self.move[0], self.source.y + self.move[1])

        if any([next_pos == (unit.x, unit.y) for unit in units]):
            return Result(ok=False, msg='Tried to move to an occupied space')

        if tiles[next_pos[0]][next_pos[1]].colliding:
            return Result(ok=False, msg='Tried to move to a colliding tile')

        self.source.x, self.source.y = next_pos
        return Result()


class LookForHeroAction(Action):
    # action specific for Enemy
    def __init__(self, source: Enemy, target: Hero) -> None:
        self.source = source
        self.target = target

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

    def perform(self, tiles: List[List[Tile]]) -> Result:
        # use obscuring to find out whether source can see target
        points = [(self.target.x, self.target.y)]

        up = self.target.x < self.source.x
        down = self.target.x > self.source.x
        left = self.target.y < self.source.y
        right = self.target.y > self.source.y

        if up:
            points.append((self.target.x - 1, self.target.y))
        if down:
            points.append((self.target.x + 1, self.target.y))
        if left:
            points.append((self.target.x, self.target.y - 1))
        if right:
            points.append((self.target.x, self.target.y + 1))

        if up and left:
            points.append((self.target.x - 1, self.target.y - 1))
        if down and left:
            points.append((self.target.x + 1, self.target.y - 1))
        if up and right:
            points.append((self.target.x - 1, self.target.y + 1))
        if down and right:
            points.append((self.target.x + 1, self.target.y + 1))

        for point in points:
            if any([
                tiles[x][y].obscuring
                for x, y
                in LookForHeroAction.__make_direct_path((self.source.x, self.source.y), point)
            ]):
                continue

            self.source.hero_seen = True
            return Result()

        return Result(ok=False, msg='Vision obscured on all possible paths')
