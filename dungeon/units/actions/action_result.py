from dataclasses import dataclass


@dataclass
class Ok:
    msg: str

@dataclass
class Fail:
    msg: str

ActionResult = Ok | Fail