from dungeon.dungeon import Dungeon

from typing import Optional


class DungeonLoader:
    @staticmethod
    def load(path: str) -> Optional[Dungeon]:
        # TODO: load a dungeon from a file of special format
        return Dungeon(map=[])
