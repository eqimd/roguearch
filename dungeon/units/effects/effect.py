from abc import ABC, abstractmethod
from typing import Any

from dungeon.units.effects.effect_enum import EffectEnum


class Effect(ABC):
    # should be overridden with effect args (specific for effect type)
    @abstractmethod
    def __init__(self, id: EffectEnum) -> None:
        self.id = id

    def apply_if_possible(self, other_id: EffectEnum, *args, **kwargs) -> Any:  # type: ignore
        return self.__apply(*args) if self.id == other_id else args

    @abstractmethod
    def __apply(self, *args, **kwargs) -> Any:  # type: ignore
        "Effect application function"
        pass
