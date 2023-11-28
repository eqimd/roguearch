
from random import random, randint
from typing import List, Tuple

from dungeon.units.actions.action import Action
from dungeon.tiles import Tile
from dungeon.units.actions.action_result import ActionResult, Fail, Ok
from dungeon.units.unit import Unit

# later add:
# UseItem
# MagicAction (?)
# ...


class AttackAction(Action):
    randomness = 0.1

    def __init__(self, source: Unit, target: Unit) -> None:
        self.source = source
        self.target = target

    def perform(self) -> ActionResult:
        # TODO: consider armor
        base_damage = (
            (2 * self.source.physical_damage)
            if random() < self.source.crit_chance
            else self.source.physical_damage
        )

        if random() > self.source.hit_chance:
            return Fail('Miss')

        if random() > self.target.dodge_chance:
            return Fail('Dodged')

        actual_damage = randint(round((1 - self.randomness) * base_damage), round((1 + self.randomness) * base_damage))

        self.target.hp = max(self.target.hp - actual_damage, 0)

        return Ok('Damaged')


class MoveAction(Action):
    def __init__(self, source: Unit, move: Tuple[int, int], units: List[Unit], tiles: List[List[Tile]]) -> None:
        self.source = source
        self.move = move
        self.units = units
        self.tiles = tiles

    def perform(self) -> ActionResult:
        next_pos = (self.source.x + self.move[0], self.source.y + self.move[1])

        if any([next_pos == (unit.x, unit.y) for unit in self.units]):
            return Fail('Tried to move to an occupied space')

        if self.tiles[next_pos[0]][next_pos[1]].colliding:
            return Fail('Tried to move to a colliding tile')

        self.source.x, self.source.y = next_pos

        return Ok('')
