"""Tests for rhasspyhermes.audioserver"""
from rhasspyhermes.audioserver import AudioFrame, AudioPlayBytes, AudioPlayFinished

site_id = "testSiteId"
request_id = "testRequestId"


def test_audio_frame():
    """Test AudioFrame."""
    assert AudioFrame.is_topic(AudioFrame.topic(site_id=site_id))
    assert AudioFrame.get_site_id(AudioFrame.topic(site_id=site_id)) == site_id


def test_audio_play_bytes():
    """Test AudioPlayBytes."""
    assert AudioPlayBytes.is_topic(
        AudioPlayBytes.topic(site_id=site_id, request_id=request_id)
    )
    assert (
        AudioPlayBytes.get_site_id(
            AudioPlayBytes.topic(site_id=site_id, request_id=request_id)
        )
        == site_id
    )
    assert (
        AudioPlayBytes.get_request_id(
            AudioPlayBytes.topic(site_id=site_id, request_id=request_id)
        )
        == request_id
    )


def test_audio_play_finished():
    """Test AudioPlayFinished."""
    assert AudioPlayFinished.is_topic(AudioPlayFinished.topic(site_id=site_id))
    assert (
        AudioPlayFinished.get_site_id(AudioPlayFinished.topic(site_id=site_id))
        == site_id
    )
