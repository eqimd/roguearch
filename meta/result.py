from dataclasses import dataclass


@dataclass
class LoadDungeon:
    path: str

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

Result = ChangeToPrevController | LoadDungeon | ForwardInput | Ok | Fail
