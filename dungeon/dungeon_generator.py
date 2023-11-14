from dungeon.dungeon import Dungeon

from typing import Optional


class DungeonGenerator:
    @staticmethod
    def generate(
        min_rooms: int,
        max_rooms: int,
        # enemy_prob: float,
        # enemy_density: float,
    ) -> Optional[Dungeon]:
        # TODO: generate a dungeon out of primitive shapes
        return Dungeon(map=[])
