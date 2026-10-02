"""Unit tests for AudioPulse configuration."""

import os
from src.audiopulse.config import AudioPulseConfig, get_api_key

def test_default_config():
    cfg = AudioPulseConfig()
    assert cfg.speaker_labels is True
    assert cfg.speakers_expected == 2
    assert cfg.sentiment_analysis is True
    assert cfg.summarization is True
    assert cfg.iab_categories is True
    assert cfg.lemur_model == "claude3_5_sonnet"

def test_custom_config():
    cfg = AudioPulseConfig(
        api_key="test-key-123",
        speakers_expected=4,
        speaker_labels=False,
    )
    assert cfg.api_key == "test-key-123"
    assert cfg.speakers_expected == 4
    assert cfg.speaker_labels is False

def test_get_api_key_from_env(monkeypatch):
    monkeypatch.setenv("ASSEMBLYAI_API_KEY", "key_abc_123")
    assert get_api_key() == "key_abc_123"

def test_get_api_key_fallback(monkeypatch):
    monkeypatch.delenv("ASSEMBLYAI_API_KEY", raising=False)
    monkeypatch.setenv("API_KEY", "legacy_key_789")
    assert get_api_key() == "legacy_key_789"
