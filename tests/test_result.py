from meta.result import Result


def test_result() -> None:
    res = Result()
    assert res.ok is True

    res.comment("test message")
    assert res.msg == "test message"

    res.fail("another test message")
    assert res.ok is False
    assert res.msg == "another test message"
