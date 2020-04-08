"""Tests for rhasspyhermes.wake"""
from rhasspyhermes.wake import HotwordDetected, HotwordToggleOff, HotwordToggleOn

wakeword_id = "testWakeWord"


def test_hotword_detected():
    """Test HotwordDetected."""
    assert HotwordDetected.is_topic(HotwordDetected.topic(wakeword_id=wakeword_id))
    assert (
        HotwordDetected.get_wakeword_id(HotwordDetected.topic(wakeword_id=wakeword_id))
        == wakeword_id
    )


def test_hotword_toggle_on():
    """Test HotwordToggleOn."""
    assert HotwordToggleOn.topic() == "hermes/hotword/toggleOn"


def test_hotword_toggle_off():
    """Test HotwordToggleOff."""
    assert HotwordToggleOff.topic() == "hermes/hotword/toggleOff"
