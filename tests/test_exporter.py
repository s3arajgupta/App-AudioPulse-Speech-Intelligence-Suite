"""Unit tests for report and JSON serialization exporters."""

from src.audiopulse.exporter import transcript_to_dict, generate_markdown_report
from src.audiopulse.mock_data import get_sample_transcript

def test_transcript_to_dict():
    t = get_sample_transcript()
    d = transcript_to_dict(t)
    assert isinstance(d, dict)
    assert d["id"] == "mock-sample-transcript-podcast-001"
    assert d["language_code"] == "en_us"
    assert len(d["utterances"]) == len(t.utterances)
    assert "sentiment_stats" in d
    assert d["sentiment_stats"]["POSITIVE"] > 0
    assert "Technology & Computing>Artificial Intelligence" in d["iab_categories"]

def test_generate_markdown_report():
    t = get_sample_transcript()
    report = generate_markdown_report(t)
    assert "# AudioPulse Intelligence Report" in report
    assert "## 1. Executive Summary" in report
    assert "## 2. Sentiment Breakdown" in report
    assert "## 3. Top IAB Content Categories" in report
    assert "## 4. Key Dialogue Timeline" in report
    assert "Speaker A" in report
