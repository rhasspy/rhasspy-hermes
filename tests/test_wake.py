"""Tests for rhasspyhermes.wake"""
from rhasspyhermes.wake import HotwordDetected, HotwordToggleOff, HotwordToggleOn

wakewordId = "testWakeWord"


def test_hotword_detected():
    """Test HotwordDetected."""
    assert HotwordDetected.is_topic(HotwordDetected.topic(wakewordId=wakewordId))
    assert (
        HotwordDetected.get_wakewordId(HotwordDetected.topic(wakewordId=wakewordId))
        == wakewordId
    )


def test_hotword_toggle_on():
    """Test HotwordToggleOn."""
    assert HotwordToggleOn.topic() == "hermes/hotword/toggleOn"


def test_hotword_toggle_off():
    """Test HotwordToggleOff."""
    assert HotwordToggleOff.topic() == "hermes/hotword/toggleOff"
