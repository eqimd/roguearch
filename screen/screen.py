from abc import ABC, abstractmethod

from typing import Any


class Screen(ABC):
    @abstractmethod
    def draw(self, *args: Any, **kwargs: Any) -> None:
        "Draws a screen from scratch"
        pass

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        "Updates an already drawn screen"
        pass
