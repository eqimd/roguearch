from dataclasses import dataclass


@dataclass
class Tile:
    symbol: str         # length 1
    colliding: bool     # blocks passage
    obscuring: bool     # blocks vision

    def __str__(self) -> str:
        return self.symbol


Empty = Tile(' ', False, False)
Floor = Tile('.', False, False)
Wall = Tile('#', True, True)
Door = Tile('D', False, True)
Exit = Tile('X', False, False)