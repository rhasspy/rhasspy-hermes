"""Tests for rhasspyhermes.asr"""
from rhasspyhermes.asr import (
    AsrStartListening,
    AsrStopListening,
    AsrTextCaptured,
    AsrToggleOff,
    AsrToggleOn,
)


def test_asr_toggle_on():
    """Test AsrToggleOn."""
    assert AsrToggleOn.topic() == "hermes/asr/toggleOn"


def test_asr_toggle_off():
    """Test AsrToggleOff."""
    assert AsrToggleOff.topic() == "hermes/asr/toggleOff"


def test_asr_start_listening():
    """Test AsrStartListening."""
    assert AsrStartListening.topic() == "hermes/asr/startListening"


def test_asr_stop_listening():
    """Test AsrStopListening."""
    assert AsrStopListening.topic() == "hermes/asr/stopListening"


def test_asr_text_captured():
    """Test AsrTextCaptured."""
    assert AsrTextCaptured.topic() == "hermes/asr/textCaptured"
