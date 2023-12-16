from abc import ABC, abstractmethod
from dungeon.dungeon import Dungeon

from dungeon.units.mobs.mob import Mob
import dungeon.units.mobs.mobs as Mobs


class MobFactory(ABC):
    @abstractmethod
    def make_mob(self, dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str) -> Mob:
        """Condition mob names corresponding to their strategies"""
        pass


class ScifiMobFactory(MobFactory):
    def make_mob(self, dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str) -> Mob:
        match strategy_name:
            case "aggressive":
                return Mobs.KillerRobot.make_mob_with_strategy_by_level(dungeon, pos_x, pos_y, level, strategy_name)
            case "coward":
                return Mobs.FaultyRobot.make_mob_with_strategy_by_level(dungeon, pos_x, pos_y, level, strategy_name)
            case "passive":
                return Mobs.Console.make_mob_with_strategy_by_level(dungeon, pos_x, pos_y, level, strategy_name)
            case _:
                return Mobs.Robot.make_basic_enemy_by_level(dungeon, pos_x, pos_y, level)


class HorrorMobFactory(MobFactory):
    def make_mob(self, dungeon: Dungeon, pos_x: int, pos_y: int, level: int, strategy_name: str) -> Mob:
        match strategy_name:
            case "aggressive":
                return Mobs.Zombie.make_mob_with_strategy_by_level(dungeon, pos_x, pos_y, level, strategy_name)
            case "coward":
                return Mobs.Ghoul.make_mob_with_strategy_by_level(dungeon, pos_x, pos_y, level, strategy_name)
            case "passive":
                return Mobs.Sleeper.make_mob_with_strategy_by_level(dungeon, pos_x, pos_y, level, strategy_name)
            case _:
                return Mobs.Ghost.make_basic_enemy_by_level(dungeon, pos_x, pos_y, level)
