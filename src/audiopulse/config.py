"""Configuration settings for AudioPulse speech intelligence platform."""

import os
from typing import Optional
from pydantic import BaseModel, Field

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class AudioPulseConfig(BaseModel):
    """AudioPulse Analysis Configuration."""
    api_key: str = Field(default="", description="AssemblyAI API Key")
    speaker_labels: bool = Field(default=True, description="Enable speaker diarization")
    speakers_expected: Optional[int] = Field(default=2, description="Expected number of speakers")
    sentiment_analysis: bool = Field(default=True, description="Enable sentence sentiment analysis")
    summarization: bool = Field(default=True, description="Enable abstractive summarization")
    iab_categories: bool = Field(default=True, description="Enable IAB content topic classification")
    language_detection: bool = Field(default=True, description="Enable automatic language detection")
    lemur_model: str = Field(default="claude3_5_sonnet", description="LeMUR model for Q&A tasks")

def get_api_key() -> str:
    """Retrieve AssemblyAI API key from environment variables."""
    return os.getenv("ASSEMBLYAI_API_KEY") or os.getenv("API_KEY") or ""
