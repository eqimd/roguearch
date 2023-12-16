from typing import Optional, Tuple

from dungeon.generator.map_generator import MapGenerator, MapGeneratorException


class MapBuilderException(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message

    def __str__(self) -> str:
        if self.message:
            msg = f'Error occurred during map loading: {self.message}'
        else:
            msg = 'An error occurred during map loading'

        return msg


class MapBuilder:
    def __init__(self):
        self.__map_generator: Optional[MapGenerator] = None

    def set_map_generator(self, generator):
        self.__map_generator = generator

    def generate(self) -> None:
        if self.__map_generator is None:
            raise Exception('Generator was not set')
        
        self.__map_generator.make_floor()
        self.__map_generator.make_doors()
        self.__map_generator.make_walls()
        self.__map_generator.make_start_exit_positions()
        # add enemies and item placement

    @property
    def tiles(self):
        if self.__map_generator is None:
            raise MapBuilderException('Generator was not set')

        return self.__map_generator.tiles

    def get_start_point(self) -> Tuple[int, int]:
        if self.__map_generator is None:
            raise MapBuilderException('Generator was not set')
        if self.__map_generator.start_point is None:
            raise MapGeneratorException('Start point was not set')
        return self.__map_generator.start_point

    def get_end_point(self) -> Tuple[int, int]:
        if self.__map_generator is None:
            raise MapBuilderException('Generator was not set')
        if self.__map_generator.end_point is None:
            raise MapGeneratorException('End point was not set')
        return self.__map_generator.end_point
