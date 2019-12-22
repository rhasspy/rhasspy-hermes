"""Tests for rhasspyhermes"""
import unittest

from rhasspyhermes.audioserver import AudioFrame, AudioPlayBytes, AudioPlayFinished
from rhasspyhermes.nlu import NluIntent
from rhasspyhermes.wake import HotwordDetected


class HermesTestCase(unittest.TestCase):
    """Tests for rhasspyhermes"""

    def test_topics(self):
        """Check get_ methods for topics"""
        siteId = "testSiteId"
        requestId = "testRequestId"
        intentName = "testIntent"
        wakewordId = "testWakeWord"

        # AudioFrame
        self.assertEqual(AudioFrame.get_siteId(AudioFrame.topic(siteId=siteId)), siteId)

        # AudioPlayBytes
        self.assertEqual(
            AudioPlayBytes.get_siteId(
                AudioPlayBytes.topic(siteId=siteId, requestId=requestId)
            ),
            siteId,
        )
        self.assertEqual(
            AudioPlayBytes.get_requestId(
                AudioPlayBytes.topic(siteId=siteId, requestId=requestId)
            ),
            requestId,
        )

        # AudioPlayFinished
        self.assertEqual(
            AudioPlayFinished.get_siteId(AudioPlayFinished.topic(siteId=siteId)), siteId
        )

        # NluIntent
        self.assertEqual(
            NluIntent.get_intentName(NluIntent.topic(intentName=intentName)), intentName
        )

        # HotwordDetected
        self.assertEqual(
            HotwordDetected.get_wakewordId(
                HotwordDetected.topic(wakewordId=wakewordId)
            ),
            wakewordId,
        )
