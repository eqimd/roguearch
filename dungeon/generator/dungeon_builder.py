from typing import Optional, Tuple

from dungeon.generator.dungeon_generator import DungeonGenerator, DungeonGeneratorException
from dungeon.units.mobs.mob_factory import MobFactory


class DungeonBuilderException(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message

    def __str__(self) -> str:
        if self.message:
            msg = f'Error occurred during map loading: {self.message}'
        else:
            msg = 'An error occurred during map loading'

        return msg


class DungeonBuilder:
    def __init__(self, level: int):
        self.__level = level
        self.__map_generator: Optional[DungeonGenerator] = None
        self.__mob_factory: Optional[MobFactory] = None

    def set_map_generator(self, generator: DungeonGenerator):
        self.__map_generator = generator
    
    def set_mob_factory(self, mob_factory: MobFactory):
        self.__mob_factory = mob_factory

    def generate(self) -> None:
        if self.__map_generator is None:
            raise Exception('Generator was not set')
        if self.__mob_factory is None:
            raise Exception('Mob factory was not set')
        
        self.__map_generator.make_floor()
        self.__map_generator.make_doors()
        self.__map_generator.make_walls()
        self.__map_generator.make_start_exit_positions()
        self.__map_generator.make_exit()
        self.__map_generator.place_mobs(self.__mob_factory, self.__level)
        # add item placement

    @property
    def dungeon(self):
        if self.__map_generator is None:
            raise DungeonBuilderException('Generator was not set')

        return self.__map_generator.dungeon

    def get_start_point(self) -> Tuple[int, int]:
        if self.__map_generator is None:
            raise DungeonBuilderException('Generator was not set')
        if self.__map_generator.start_point is None:
            raise DungeonGeneratorException('Start point was not set')
        return self.__map_generator.start_point

    def get_end_point(self) -> Tuple[int, int]:
        if self.__map_generator is None:
            raise DungeonBuilderException('Generator was not set')
        if self.__map_generator.end_point is None:
            raise DungeonGeneratorException('End point was not set')
        return self.__map_generator.end_point
