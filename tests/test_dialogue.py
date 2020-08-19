"""Tests for rhasspyhermes.dialogue"""
from rhasspyhermes.dialogue import (
    DialogueContinueSession,
    DialogueEndSession,
    DialogueIntentNotRecognized,
    DialogueSessionEnded,
    DialogueSessionQueued,
    DialogueSessionStarted,
    DialogueStartSession,
)


def test_dialogue_continue_session():
    """Test DialogueContinueSession."""
    assert DialogueContinueSession.topic() == "hermes/dialogueManager/continueSession"


def test_dialogue_end_session():
    """Test DialogueEndSession."""
    assert DialogueEndSession.topic() == "hermes/dialogueManager/endSession"


def test_dialogue_intent_not_recognized():
    """Test DialogueIntentNotRecognized."""
    assert (
        DialogueIntentNotRecognized.topic()
        == "hermes/dialogueManager/intentNotRecognized"
    )


def test_dialogue_session_ended():
    """Test DialogueSessionEnded."""
    assert DialogueSessionEnded.topic() == "hermes/dialogueManager/sessionEnded"


def test_dialogue_session_queued():
    """Test DialogueSessionQueued."""
    assert DialogueSessionQueued.topic() == "hermes/dialogueManager/sessionQueued"


def test_dialogue_session_started():
    """Test DialogueSessionStarted."""
    assert DialogueSessionStarted.topic() == "hermes/dialogueManager/sessionStarted"


def test_dialogue_start_session():
    """Test DialogueStartSession."""
    assert DialogueStartSession.topic() == "hermes/dialogueManager/startSession"
