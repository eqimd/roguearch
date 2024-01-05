import copy
import random

from dungeon.dungeon import Dungeon
from dungeon.units.mobs.mob_prototype import MobPrototype


class KillerRobot(MobPrototype):
    @property
    def name(self) -> str:
        return 'Killer Robot'

    @staticmethod
    def make_mob_with_strategy_by_level(dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str):
        return KillerRobot(
            dungeon=dungeon,
            pos_x=pos_x,
            pos_y=pos_y,
            max_hp=10 + 2 * level,
            max_mp=0,
            exp_points=level + 1,
            hit_chance=0.8,
            crit_chance=0.1,
            physical_damage=2 + level,
            magical_damage=0,
            dodge_chance=0.1,
            bleed_resistance=0.2,
            poison_resistance=0.2,
            debuff_resistance=0.2,
            hero_seen=False,
            strategy_name=strategy_name,
        )


class FaultyRobot(MobPrototype):
    @property
    def name(self) -> str:
        return 'Faulty Robot'

    @staticmethod
    def make_mob_with_strategy_by_level(dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str):
        return FaultyRobot(
            dungeon=dungeon,
            pos_x=pos_x,
            pos_y=pos_y,
            max_hp=10 + 2 * level,
            max_mp=0,
            exp_points=level + 1,
            hit_chance=0.8,
            crit_chance=0.1,
            physical_damage=2 + level,
            magical_damage=0,
            dodge_chance=0.1,
            bleed_resistance=0.2,
            poison_resistance=0.2,
            debuff_resistance=0.2,
            hero_seen=False,
            strategy_name=strategy_name,
        )


class Console(MobPrototype):
    @property
    def name(self) -> str:
        return 'Console'

    @staticmethod
    def make_mob_with_strategy_by_level(dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str):
        return Console(
            dungeon=dungeon,
            pos_x=pos_x,
            pos_y=pos_y,
            max_hp=10 + 2 * level,
            max_mp=0,
            exp_points=level + 1,
            hit_chance=0.8,
            crit_chance=0.1,
            physical_damage=2 + level,
            magical_damage=0,
            dodge_chance=0.1,
            bleed_resistance=0.2,
            poison_resistance=0.2,
            debuff_resistance=0.2,
            hero_seen=False,
            strategy_name=strategy_name,
        )


class Robot(MobPrototype):
    @property
    def name(self) -> str:
        return 'Robot'

    @staticmethod
    def make_mob_with_strategy_by_level(dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str):
        return Robot(
            dungeon=dungeon,
            pos_x=pos_x,
            pos_y=pos_y,
            max_hp=10 + 2 * level,
            max_mp=0,
            exp_points=level + 1,
            hit_chance=0.8,
            crit_chance=0.1,
            physical_damage=2 + level,
            magical_damage=0,
            dodge_chance=0.1,
            bleed_resistance=0.2,
            poison_resistance=0.2,
            debuff_resistance=0.2,
            hero_seen=False,
            strategy_name=strategy_name,
        )


class Zombie(MobPrototype):
    @property
    def name(self) -> str:
        return 'Killer Robot'

    @staticmethod
    def make_mob_with_strategy_by_level(dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str):
        return Zombie(
            dungeon=dungeon,
            pos_x=pos_x,
            pos_y=pos_y,
            max_hp=10 + 2 * level,
            max_mp=0,
            exp_points=level + 1,
            hit_chance=0.8,
            crit_chance=0.1,
            physical_damage=2 + level,
            magical_damage=0,
            dodge_chance=0.1,
            bleed_resistance=0.2,
            poison_resistance=0.2,
            debuff_resistance=0.2,
            hero_seen=False,
            strategy_name=strategy_name,
        )


class Ghoul(MobPrototype):
    @property
    def name(self) -> str:
        return 'Faulty Robot'

    @staticmethod
    def make_mob_with_strategy_by_level(dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str):
        return Ghoul(
            dungeon=dungeon,
            pos_x=pos_x,
            pos_y=pos_y,
            max_hp=10 + 2 * level,
            max_mp=0,
            exp_points=level + 1,
            hit_chance=0.8,
            crit_chance=0.1,
            physical_damage=2 + level,
            magical_damage=0,
            dodge_chance=0.1,
            bleed_resistance=0.2,
            poison_resistance=0.2,
            debuff_resistance=0.2,
            hero_seen=False,
            strategy_name=strategy_name,
        )


class Sleeper(MobPrototype):
    @property
    def name(self) -> str:
        return 'Console'

    @staticmethod
    def make_mob_with_strategy_by_level(dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str):
        return Sleeper(
            dungeon=dungeon,
            pos_x=pos_x,
            pos_y=pos_y,
            max_hp=10 + 2 * level,
            max_mp=0,
            exp_points=level + 1,
            hit_chance=0.8,
            crit_chance=0.1,
            physical_damage=2 + level,
            magical_damage=0,
            dodge_chance=0.1,
            bleed_resistance=0.2,
            poison_resistance=0.2,
            debuff_resistance=0.2,
            hero_seen=False,
            strategy_name=strategy_name,
        )


class Ghost(MobPrototype):
    @property
    def name(self) -> str:
        return 'Robot'

    @staticmethod
    def make_mob_with_strategy_by_level(dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str):
        return Ghost(
            dungeon=dungeon,
            pos_x=pos_x,
            pos_y=pos_y,
            max_hp=10 + 2 * level,
            max_mp=0,
            exp_points=level + 1,
            hit_chance=0.8,
            crit_chance=0.1,
            physical_damage=2 + level,
            magical_damage=0,
            dodge_chance=0.1,
            bleed_resistance=0.2,
            poison_resistance=0.2,
            debuff_resistance=0.2,
            hero_seen=False,
            strategy_name=strategy_name,
        )


# mob that multiplies with a given probability
class ToxicMold(MobPrototype):

    _p_duplicate = 0.1

    def set_p_duplicate(self, p: float):
        self._p_duplicate = p

    def clone(self, **attrs):
        if random.random() > self._p_duplicate:
            return
        neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbours = list(filter(lambda d:
                                 self.dungeon.is_empty_floor_tile(self.x + d[0], self.y + d[1]), neighbours))
        if len(neighbours) == 0:
            return

        random.shuffle(neighbours)
        dx, dy = neighbours[0]
        copied = copy.deepcopy(self)
        copied.x = self.x + dx
        copied.y = self.y + dy
        self.dungeon.units.append(copied)

    @property
    def name(self) -> str:
        return 'Toxic Mold'

    @staticmethod
    def make_mob_with_strategy_by_level(dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str) -> MobPrototype:
        return ToxicMold(
            dungeon=dungeon,
            pos_x=pos_x,
            pos_y=pos_y,
            max_hp=10 + 2 * level,
            max_mp=0,
            exp_points=level + 1,
            hit_chance=0.8,
            crit_chance=0.1,
            physical_damage=2 + level,
            magical_damage=0,
            dodge_chance=0.1,
            bleed_resistance=0.2,
            poison_resistance=0.2,
            debuff_resistance=0.2,
            hero_seen=False,
            strategy_name=strategy_name,
            symbol_seen='0',
            symbol_not_seen='s'
        )
