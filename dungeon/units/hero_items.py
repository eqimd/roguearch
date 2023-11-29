from dungeon.units.entity import Entity


class Sword(Entity):
    def symbol(self) -> str:
        return '!'