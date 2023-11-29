from dungeon.units.items.wearable.weapon import Weapon


class ActiveInventory:
    def __init__(self, weapon: Weapon):
        self.weapon = weapon