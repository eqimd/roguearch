from typing import Optional


class Result:
    def __init__(self, ok: Optional[bool] = True, msg: Optional[str] = "") -> None:
        self.ok = ok
        self.msg = msg

    def fail(self, msg: Optional[str] = "") -> None:
        self.ok = False
        self.msg = msg

    def comment(self, msg: Optional[str] = "") -> None:
        self.msg = msg
