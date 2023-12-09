from math import sqrt
from random import random, randint, shuffle
from typing import List, Tuple, cast
from dungeon.dungeon import Dungeon
from dungeon.inventory import Inventory

from dungeon.units.actions.action import Action
from dungeon.tiles import Tile, Exit
from dungeon.units.actions.action_result import ActionResult, Fail, Ok
from dungeon.units.hero import Hero
from dungeon.units.items.item import Item, ItemOnScreen
from dungeon.units.mobs.base_mob import BaseMob
from dungeon.units.mobs.mob import Mob
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

        if random() <= self.target.dodge_chance:
            return Fail('Dodged')

        actual_damage = randint(round((1 - self.randomness) * base_damage), round((1 + self.randomness) * base_damage))

        d_x = abs(self.source.x - self.target.x)
        d_y = abs(self.source.y - self.target.y)

        actual_damage /= sqrt(d_x * d_x + d_y * d_y)

        actual_damage = round(actual_damage)

        self.target.hp = max(self.target.hp - actual_damage, 0)

        if self.target.hp == 0 and issubclass(type(self.source), Hero):
            exp_points = cast(Mob, self.target).exp_points
            cast(Hero, self.source).add_exp_points(exp_points)
            return Ok('Killed')

        if issubclass(type(self.target), Mob) and actual_damage > 0:
            mob = cast(Mob, self.target)
            mob.dungeon.units.remove(self.target)
            mob.dungeon.units.append(EmbarrassmentMobDecorator(mob, 2))

        return Ok('Damaged')


class MoveAction(Action):
    def __init__(self, source: Unit, move: Tuple[int, int], dungeon: Dungeon) -> None:
        self.source = source
        self.move = move
        self.dungeon = dungeon

    def perform(self) -> ActionResult:
        if self.move[0] == 0 and self.move[1] == 0:
            return Ok("Do nothing")

        next_pos = (self.source.x + self.move[0], self.source.y + self.move[1])

        if any([next_pos == (unit.x, unit.y) for unit in self.dungeon.units]):
            # происходит сражение
            opponent = filter(lambda unit: next_pos == (unit.x, unit.y), self.dungeon.units).__next__()
            return AttackAction(self.source, opponent).perform()

        if next_pos == (self.dungeon.hero.x, self.dungeon.hero.y):
            return AttackAction(self.source, self.dungeon.hero).perform()

        if self.dungeon.map[next_pos[0]][next_pos[1]].colliding:
            return Fail('Tried to move to a colliding tile')

        self.source.x, self.source.y = next_pos

        if self.dungeon.map[self.source.x][self.source.y] is Exit:
            return Ok('You WIN!')

        item = next((itm for itm in self.dungeon.items if itm.x == next_pos[0] and itm.y == next_pos[1]), None)
        if item is not None:
            return Ok(item.item.description)

        return Ok('')


class PickupAction(Action):
    def __init__(self, inventory: Inventory, item: ItemOnScreen, dungeon: Dungeon):
        self.inventory = inventory
        self.item = item
        self.dungeon = dungeon

    def perform(self) -> ActionResult:
        ok = self.inventory.add_item(self.item.item)

        if ok:
            self.dungeon.items.remove(self.item)

            return Ok('Added ' + self.item.item.description + ' to inventory')
        else:
            return Fail('Can\'t add item: inventory is full')


# декоратор, добавляющий конфузию
class EmbarrassmentMobDecorator(BaseMob, Unit):
    def __init__(self, mob: Mob, embarrassment_level: int):
        self.mob = mob
        self.embarrassment_level = embarrassment_level

    def perform_action(self) -> ActionResult:
        if self.embarrassment_level <= 0:
            self.mob.dungeon.units.append(self.mob)
            self.mob.dungeon.units.remove(self)
            return self.mob.perform_action()

        self.embarrassment_level -= 1
        moves = [(x, y) for x in [-1, 1] for y in [-1, 0, 1]] + [(y, x) for x in [-1, 1] for y in [-1, 0, 1]]
        shuffle(moves)
        return MoveAction(self, moves[0], self.mob.dungeon).perform()

    @property
    def x(self):
        return self.mob.x

    @x.setter
    def x(self, value):
        self.mob.x = value

    @property
    def y(self) -> int:
        return self.mob.y

    @y.setter
    def y(self, value):
        self.mob.y = value

    @property
    def hp(self) -> int:
        return self.mob.hp

    @hp.setter
    def hp(self, value):
        self.mob.hp = value

    @property
    def mp(self) -> int:
        return self.mob.mp

    @mp.setter
    def mp(self, value):
        self.mob.mp = value

    @property
    def exp_points(self) -> int:
        return self.mob.exp_points

    @property
    def max_hp(self) -> int:
        return self.mob.max_hp

    @property
    def max_mp(self) -> int:
        return self.mob.max_mp

    @property
    def hit_chance(self) -> float:
        return self.mob.hit_chance

    @property
    def crit_chance(self) -> float:
        return self.mob.crit_chance

    @property
    def physical_damage(self) -> int:
        return self.mob.physical_damage

    @property
    def magical_damage(self) -> int:
        return self.mob.magical_damage

    @property
    def dodge_chance(self) -> float:
        return self.mob.dodge_chance

    @property
    def bleed_resistance(self) -> float:
        return self.mob.bleed_resistance

    @property
    def poison_resistance(self) -> float:
        return self.mob.poison_resistance

    @property
    def debuff_resistance(self) -> float:
        return self.mob.debuff_resistance

    @property
    def symbol(self) -> str:
        return self.mob.symbol
