"""Tests for rhasspyhermes.audioserver"""
from rhasspyhermes.audioserver import AudioFrame, AudioPlayBytes, AudioPlayFinished

siteId = "testSiteId"
requestId = "testRequestId"


def test_audio_frame():
    """Test AudioFrame."""
    assert AudioFrame.is_topic(AudioFrame.topic(siteId=siteId))
    assert AudioFrame.get_siteId(AudioFrame.topic(siteId=siteId)) == siteId


def test_audio_play_bytes():
    """Test AudioPlayBytes."""
    assert AudioPlayBytes.is_topic(
        AudioPlayBytes.topic(siteId=siteId, requestId=requestId)
    )
    assert (
        AudioPlayBytes.get_siteId(
            AudioPlayBytes.topic(siteId=siteId, requestId=requestId)
        )
        == siteId
    )
    assert (
        AudioPlayBytes.get_requestId(
            AudioPlayBytes.topic(siteId=siteId, requestId=requestId)
        )
        == requestId
    )


def test_audio_play_finished():
    """Test AudioPlayFinished."""
    assert AudioPlayFinished.is_topic(AudioPlayFinished.topic(siteId=siteId))
    assert (
        AudioPlayFinished.get_siteId(AudioPlayFinished.topic(siteId=siteId)) == siteId
    )
