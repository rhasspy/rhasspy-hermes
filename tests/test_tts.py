"""Tests for rhasspyhermes.tts"""
from rhasspyhermes.tts import TtsSay, TtsSayFinished


def test_tts_say():
    """Test TtsSay."""
    assert TtsSay.topic() == "hermes/tts/say"


def test_tts_say_finished():
    """Test TtsSayFinished."""
    assert TtsSayFinished.topic() == "hermes/tts/sayFinished"
