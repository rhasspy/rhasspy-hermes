"""Tests for rhasspyhermes.handle"""
from rhasspyhermes.handle import HandleToggleOff, HandleToggleOn


def test_handle_toggle_off():
    """Test HandleToggleOff."""
    assert HandleToggleOff.topic() == "rhasspy/handle/toggleOff"
    assert HandleToggleOff().payload() == '{"siteId": "default"}'


def test_handle_toggle_on():
    """Test HandleToggleOn."""
    assert HandleToggleOn.topic() == "rhasspy/handle/toggleOn"
    assert HandleToggleOn(site_id="satellite").payload() == '{"siteId": "satellite"}'
