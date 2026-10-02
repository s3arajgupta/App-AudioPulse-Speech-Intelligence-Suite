"""Unit tests for mock sample transcript data."""

from src.audiopulse.mock_data import get_sample_transcript, MockTranscript

def test_mock_transcript_properties():
    t = get_sample_transcript()
    assert isinstance(t, MockTranscript)
    assert t.audio_duration > 0
    assert t.language_code == "en_us"
    assert len(t.utterances) >= 5
    assert len(t.sentiment_analysis) >= 5
    assert len(t.iab_categories.summary) >= 3
    assert len(t.summary) > 20

def test_mock_get_sentences():
    t = get_sample_transcript()
    sentences = t.get_sentences()
    assert len(sentences) == len(t.sentiment_analysis)
    assert sentences[0].text == t.sentiment_analysis[0].text
