"""Tests for rhasspyhermes"""
from rhasspyhermes.audioserver import AudioFrame, AudioPlayBytes, AudioPlayFinished

from rhasspyhermes.nlu import NluIntent
from rhasspyhermes.wake import HotwordDetected


def test_topics():
    """Check get_ methods for topics"""
    siteId = "testSiteId"
    requestId = "testRequestId"
    intentName = "testIntent"
    wakewordId = "testWakeWord"

    # AudioFrame
    assert AudioFrame.is_topic(AudioFrame.topic(siteId=siteId))
    assert AudioFrame.get_siteId(AudioFrame.topic(siteId=siteId)) == siteId

    # AudioPlayBytes
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

    # AudioPlayFinished
    assert AudioPlayFinished.is_topic(AudioPlayFinished.topic(siteId=siteId))
    assert (
        AudioPlayFinished.get_siteId(AudioPlayFinished.topic(siteId=siteId)) == siteId
    )

    # NluIntent
    assert NluIntent.is_topic(NluIntent.topic(intentName=intentName))
    assert (
        NluIntent.get_intentName(NluIntent.topic(intentName=intentName)) == intentName
    )

    # HotwordDetected
    assert HotwordDetected.is_topic(HotwordDetected.topic(wakewordId=wakewordId))
    assert (
        HotwordDetected.get_wakewordId(HotwordDetected.topic(wakewordId=wakewordId))
        == wakewordId
    )
