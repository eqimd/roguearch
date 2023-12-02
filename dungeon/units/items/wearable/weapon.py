from dataclasses import dataclass
from dungeon.units.items.item_enum import ItemEnum

from dungeon.units.items.wearable.wearable_item import WearableItem


@dataclass
class Weapon(WearableItem):
    damage: int
    magic: int

    symbol_self: str = '!'

    def __init__(self) -> None:
        self.id = ItemEnum.Weapon

    @property
    def symbol(self) -> str:
        return Weapon.symbol_self


class WeaponArthurSword(Weapon):
    def __init__(self) -> None:
        super().__init__()

        self.damage = 5
        self.magic = 5
        self.weight = 0
        self.effects = []

    @property
    def symbol(self) -> str:
        return '!'

    @property
    def description(self) -> str:
        return 'Arthur\'s sword.'

class WeaponFinka(Weapon):
    def __init__(self) -> None:
        super().__init__()

        self.damage = 1
        self.magic = 0
        self.weight = 0
        self.effects = []

    @property
    def symbol(self) -> str:
        return '\\'
    
    @property
    def description(self) -> str:
        return 'Just a finka. Cheeky breeky.'    
