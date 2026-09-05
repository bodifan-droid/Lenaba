
from scripts.lib.confidence import can_verify


def test_confidence_gate():

    assert can_verify(1.0)
    assert can_verify(0.95)
    assert can_verify(0.90)

    assert not can_verify(0.89)
    assert not can_verify(None)

    assert can_verify(None, manual=True)