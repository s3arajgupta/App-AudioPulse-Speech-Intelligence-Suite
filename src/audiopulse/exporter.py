"""Export utilities for audio intelligence results (JSON & Markdown)."""

import json
from typing import Any, Dict
from .transcriber import timestamp_string, calculate_sentiment_stats

def transcript_to_dict(transcript: Any) -> Dict[str, Any]:
    """Convert an AssemblyAI or Mock transcript object into a serialized dictionary."""
    utterances = []
    for u in getattr(transcript, "utterances", []):
        utterances.append({
            "speaker": getattr(u, "speaker", "A"),
            "text": getattr(u, "text", ""),
            "start_ms": getattr(u, "start", 0),
            "end_ms": getattr(u, "end", 0),
            "start_time": timestamp_string(getattr(u, "start", 0)),
            "end_time": timestamp_string(getattr(u, "end", 0))
        })

    sentiments = []
    for s in getattr(transcript, "sentiment_analysis", []):
        sentiments.append({
            "speaker": getattr(s, "speaker", "A"),
            "text": getattr(s, "text", ""),
            "sentiment": getattr(s, "sentiment", "NEUTRAL"),
            "start_time": timestamp_string(getattr(s, "start", 0))
        })

    iab_summary = {}
    if hasattr(transcript, "iab_categories") and hasattr(transcript.iab_categories, "summary"):
        iab_summary = dict(transcript.iab_categories.summary)

    return {
        "id": getattr(transcript, "id", "transcript-001"),
        "status": getattr(transcript, "status", "completed"),
        "language_code": getattr(transcript, "language_code", "en_us"),
        "duration_seconds": getattr(transcript, "audio_duration", 0),
        "summary": getattr(transcript, "summary", ""),
        "full_text": getattr(transcript, "text", ""),
        "sentiment_stats": calculate_sentiment_stats(transcript),
        "iab_categories": iab_summary,
        "utterances": utterances,
        "sentiments": sentiments
    }

def generate_markdown_report(transcript: Any) -> str:
    """Generate a clean executive Markdown report summarizing audio analysis."""
    data = transcript_to_dict(transcript)
    stats = data["sentiment_stats"]

    report = f"""# AudioPulse Intelligence Report

**Transcript ID:** `{data['id']}`  
**Language:** {data['language_code'].upper()}  
**Duration:** {timestamp_string(data['duration_seconds'] * 1000)}  

---

## 1. Executive Summary
{data['summary']}

---

## 2. Sentiment Breakdown
- **Positive Sentences:** {stats['POSITIVE']} ({stats['positive_pct']}%)
- **Neutral Sentences:** {stats['NEUTRAL']} ({stats['neutral_pct']}%)
- **Negative Sentences:** {stats['NEGATIVE']} ({stats['negative_pct']}%)

---

## 3. Top IAB Content Categories
"""
    for topic, relevance in sorted(data['iab_categories'].items(), key=lambda x: x[1], reverse=True):
        report += f"- **{topic}**: {round(relevance * 100, 1)}%\n"

    report += "\n---\n\n## 4. Key Dialogue Timeline\n"
    for u in data['utterances'][:10]:
        report += f"- `[{u['start_time']}]` **Speaker {u['speaker']}:** {u['text']}\n"

    report += "\n*Generated automatically by AudioPulse Speech Intelligence Suite.*"
    return report
