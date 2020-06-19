"""Tests for rhasspyhermes.handle"""
from rhasspyhermes.handle import HandleToggleOff, HandleToggleOn


def test_handle_toggle_off():
    """Test HandleToggleOff."""
    assert HandleToggleOff.topic() == "rhasspy/handle/toggleOff"


def test_handle_toggle_on():
    """Test HandleToggleOn."""
    assert HandleToggleOn.topic() == "rhasspy/handle/toggleOn"
