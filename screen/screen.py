from abc import ABC, abstractmethod

from typing import Any

from blessed import Terminal


class Screen(ABC):
    @abstractmethod
    def draw(self, *args: Any, **kwargs: Any) -> None:
        "Draws a screen from scratch"
        pass

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> None:
        "Updates an already drawn screen"
        pass

    @classmethod
    def flush(cls, terminal: Terminal):
        print(terminal.clear + terminal.move_xy(0, terminal.height - 1), end='')