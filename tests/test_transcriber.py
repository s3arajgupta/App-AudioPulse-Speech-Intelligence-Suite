"""Unit tests for AudioPulse transcription and sentiment utilities."""

from src.audiopulse.transcriber import (
    timestamp_string,
    calculate_sentiment_stats,
    transcribe_audio,
)
from src.audiopulse.mock_data import get_sample_transcript, MockSentiment

def test_timestamp_string_zero():
    assert timestamp_string(0) == "00:00:00"

def test_timestamp_string_minutes():
    # 65,000 ms = 1 min 5 sec
    assert timestamp_string(65000) == "00:01:05"

def test_timestamp_string_hours():
    # 3,661,000 ms = 1 hr 1 min 1 sec
    assert timestamp_string(3661000) == "01:01:01"

def test_calculate_sentiment_stats_empty():
    class DummyEmpty:
        sentiment_analysis = []
    
    stats = calculate_sentiment_stats(DummyEmpty())
    assert stats["total"] == 0
    assert stats["positive_pct"] == 0.0

def test_calculate_sentiment_stats_breakdown():
    class DummyTranscript:
        sentiment_analysis = [
            MockSentiment("A", "Great job!", "POSITIVE", 0, 1000),
            MockSentiment("B", "I agree.", "POSITIVE", 1000, 2000),
            MockSentiment("A", "This is okay.", "NEUTRAL", 2000, 3000),
            MockSentiment("B", "That failed.", "NEGATIVE", 3000, 4000),
        ]

    stats = calculate_sentiment_stats(DummyTranscript())
    assert stats["total"] == 4
    assert stats["POSITIVE"] == 2
    assert stats["NEUTRAL"] == 1
    assert stats["NEGATIVE"] == 1
    assert stats["positive_pct"] == 50.0
    assert stats["neutral_pct"] == 25.0
    assert stats["negative_pct"] == 25.0

def test_transcribe_audio_force_mock():
    res = transcribe_audio("dummy.mp3", force_mock=True)
    assert res is not None
    assert len(res.utterances) > 0
    assert "Universal-1" in res.text
