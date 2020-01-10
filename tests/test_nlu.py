"""Tests for rhasspyhermes.nlu"""
from rhasspyhermes.nlu import NluError, NluIntent, NluIntentNotRecognized, NluQuery

intentName = "testIntent"


def test_nlu_intent():
    """Test NluIntent."""
    assert NluIntent.is_topic(NluIntent.topic(intentName=intentName))
    assert (
        NluIntent.get_intentName(NluIntent.topic(intentName=intentName)) == intentName
    )


def test_nlu_query():
    """Test NluQuery."""
    assert NluQuery.topic() == "hermes/nlu/query"


def test_nlu_intent_not_Recognized():
    """Test NluIntentNotRecognized."""
    assert NluIntentNotRecognized.topic() == "hermes/nlu/intentNotRecognized"


def test_nlu_error():
    """Test NluError."""
    assert NluError.topic() == "hermes/error/nlu"
