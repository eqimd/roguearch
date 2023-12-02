from enum import Enum


class ItemEnum(Enum):
    Weapon = 0      # weapon
    UpperBody = 1   # upper body armor
    LowerBody = 2   # lower body armor
    Ring = 3        # trinket
    Amulet = 4      # trinket
    Potion = 90     # replenishes HP
    Ether = 91      # replenishes MP
    Bandage = 92    # heals bleeding
    Antidote = 93   # heals poisoning
    Herb = 94       # removes debuffs
