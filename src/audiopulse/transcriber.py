"""Audio Transcription and Intelligence extraction engine."""

from typing import Dict, Any, Optional
from .config import AudioPulseConfig, get_api_key
from .mock_data import get_sample_transcript, MockTranscript

def timestamp_string(milliseconds: int) -> str:
    """Convert millisecond timestamp into HH:MM:SS format."""
    seconds = milliseconds // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def calculate_sentiment_stats(transcript: Any) -> Dict[str, Any]:
    """Calculate sentiment breakdown counts and percentages."""
    sentiments = getattr(transcript, "sentiment_analysis", [])
    if not sentiments:
        return {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0, "total": 0, "positive_pct": 0.0, "neutral_pct": 0.0, "negative_pct": 0.0}

    counts = {"POSITIVE": 0, "NEUTRAL": 0, "NEGATIVE": 0}
    for item in sentiments:
        s = getattr(item, "sentiment", "NEUTRAL")
        counts[s] = counts.get(s, 0) + 1

    total = len(sentiments)
    return {
        "POSITIVE": counts["POSITIVE"],
        "NEUTRAL": counts["NEUTRAL"],
        "NEGATIVE": counts["NEGATIVE"],
        "total": total,
        "positive_pct": round((counts["POSITIVE"] / total) * 100, 1) if total > 0 else 0.0,
        "neutral_pct": round((counts["NEUTRAL"] / total) * 100, 1) if total > 0 else 0.0,
        "negative_pct": round((counts["NEGATIVE"] / total) * 100, 1) if total > 0 else 0.0,
    }

def transcribe_audio(
    audio_file_or_path: Any,
    config: Optional[AudioPulseConfig] = None,
    api_key: Optional[str] = None,
    force_mock: bool = False
) -> Any:
    """Transcribe an audio file using AssemblyAI or return mock transcript.
    
    Args:
        audio_file_or_path: File object or local file path
        config: AudioPulseConfig instance
        api_key: AssemblyAI API key (optional if in env)
        force_mock: Force offline mock transcript
    """
    key = api_key or get_api_key()
    cfg = config or AudioPulseConfig()

    if force_mock or not key:
        return get_sample_transcript()

    try:
        import assemblyai as aai
        aai.settings.api_key = key

        transcription_config = aai.TranscriptionConfig(
            speaker_labels=cfg.speaker_labels,
            speakers_expected=cfg.speakers_expected,
            iab_categories=cfg.iab_categories,
            sentiment_analysis=cfg.sentiment_analysis,
            summarization=cfg.summarization,
            language_detection=cfg.language_detection
        )

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file_or_path, config=transcription_config)
        return transcript
    except Exception as e:
        print(f"Warning: Live AssemblyAI transcription failed ({e}). Falling back to sample transcript.")
        return get_sample_transcript()
