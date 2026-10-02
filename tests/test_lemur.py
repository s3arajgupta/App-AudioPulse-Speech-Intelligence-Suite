"""Unit tests for LeMUR conversational query agent."""

from src.audiopulse.lemur_agent import query_lemur
from src.audiopulse.mock_data import get_sample_transcript

def test_query_lemur_empty_prompt():
    t = get_sample_transcript()
    res = query_lemur(t, "")
    assert "Please enter a valid question" in res

def test_query_lemur_summary_prompt():
    t = get_sample_transcript()
    res = query_lemur(t, "Give me a summary of this conversation")
    assert "discussion" in res.lower() or "speech" in res.lower()

def test_query_lemur_sentiment_prompt():
    t = get_sample_transcript()
    res = query_lemur(t, "What is the sentiment tone?")
    assert "positive" in res.lower()

def test_query_lemur_none_transcript():
    res = query_lemur(None, "Any question")
    assert "not available" in res.lower()
