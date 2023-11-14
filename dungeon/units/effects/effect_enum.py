from enum import Enum


class EffectEnum(Enum):
    HPOffset = 0
    HPMultiplier = 1
    MPOffset = 10
    MPMultiplier = 11
    AccOffset = 20
    CritMultiplier = 30
    BleedResMultiplier = 90
    PoisonResMultiplier = 91
    DebuffResMultiplier = 92
