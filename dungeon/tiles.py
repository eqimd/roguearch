from dataclasses import dataclass

from dungeon.tile_enum import TileEnum


@dataclass
class Tile:
    id: TileEnum
    symbol: str         # length 1
    colliding: bool     # blocks passage
    obscuring: bool     # blocks vision


Floor = Tile(TileEnum.Floor, '.', False, False)
Wall = Tile(TileEnum.Wall, '#', True, True)
Door = Tile(TileEnum.Door, 'D', False, True)
