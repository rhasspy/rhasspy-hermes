"""Tests for rhasspyhermes.nlu"""
from rhasspyhermes.nlu import NluError, NluIntent, NluIntentNotRecognized, NluQuery

intent_name = "testIntent"


def test_nlu_intent():
    """Test NluIntent."""
    assert NluIntent.is_topic(NluIntent.topic(intent_name=intent_name))
    assert (
        NluIntent.get_intent_name(NluIntent.topic(intent_name=intent_name))
        == intent_name
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
