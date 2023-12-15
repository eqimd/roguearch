from typing import Optional

from dungeon.generator.map_generator import MapGenerator


class DungeonGenerator:
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
        # add enemies and item placement

    @property
    def tiles(self):
        if self.__map_generator is None:
            raise Exception('Generator was not set')

        return self.__map_generator.tiles
