from dataclasses import dataclass


@dataclass
class Fail:
    msg: str


@dataclass
class Ok:
    msg: str


@dataclass
class ForwardInput:
    pass


@dataclass
class ChangeToPrevController:
    pass


@dataclass
class ChangeToNextController:
    pass


Result = ChangeToNextController | ChangeToPrevController | ForwardInput | Ok | Fail
