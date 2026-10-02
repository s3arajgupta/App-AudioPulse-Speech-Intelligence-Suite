"""Offline Mock Data Provider for AudioPulse.
Provides pre-computed analysis for the bundled sample podcast (podcast.mp3),
allowing instant demonstration and automated testing without an AssemblyAI API key.
"""

from typing import List, Dict, Any

class MockUtterance:
    def __init__(self, speaker: str, text: str, start: int, end: int):
        self.speaker = speaker
        self.text = text
        self.start = start
        self.end = end

class MockSentiment:
    def __init__(self, speaker: str, text: str, sentiment: str, start: int, end: int):
        self.speaker = speaker
        self.text = text
        self.sentiment = sentiment
        self.start = start
        self.end = end

class MockSentence:
    def __init__(self, text: str, start: int, end: int, speaker: str = "A"):
        self.text = text
        self.start = start
        self.end = end
        self.speaker = speaker

class MockIABCategories:
    def __init__(self, summary: Dict[str, float]):
        self.summary = summary

class MockLemurResponse:
    def __init__(self, response: str):
        self.response = response

class MockLemur:
    def __init__(self, transcript: "MockTranscript"):
        self.transcript = transcript

    def task(self, prompt: str, final_model: Any = None) -> MockLemurResponse:
        prompt_lower = prompt.lower()
        if "summary" in prompt_lower or "about" in prompt_lower:
            ans = "The podcast conversation explores advancements in speech recognition, multimodal generative AI, developer APIs, and how voice interfaces are transforming digital workflows."
        elif "speaker" in prompt_lower or "who" in prompt_lower:
            ans = "The discussion features two speakers: the podcast host (Speaker A) and a guest AI researcher (Speaker B) discussing next-generation speech models."
        elif "sentiment" in prompt_lower:
            ans = "The overall sentiment of the episode is predominantly positive (72%), driven by enthusiastic discussions about AI developer productivity and model accuracy."
        elif "universal-1" in prompt_lower or "model" in prompt_lower:
            ans = "They highlighted Universal-1, which achieves over 10% accuracy improvements in multilingual transcription and a 30% reduction in hallucination rates compared to Whisper Large-v3."
        else:
            ans = f"Based on the transcript analysis: {self.transcript.summary}"
        return MockLemurResponse(ans)

class MockTranscript:
    def __init__(self):
        self.id = "mock-sample-transcript-podcast-001"
        self.status = "completed"
        self.audio_duration = 345  # 5 minutes 45 seconds
        self.language_code = "en_us"
        self.text = (
            "Welcome back to the podcast. Today we are diving into speech AI, speech-to-text models, "
            "and how developer APIs are revolutionizing audio analysis. In recent benchmarks, "
            "multimodal speech architectures like Universal-1 have demonstrated a 10% accuracy gain "
            "and 30% fewer hallucinations than previous baselines. We also examine LeMUR, which enables "
            "direct natural language question-answering over conversational transcripts without custom RAG pipelines."
        )
        self.summary = (
            "This podcast episode discusses the rapid evolution of speech-to-text AI models. "
            "The speakers examine benchmarks comparing next-generation architectures like Universal-1 "
            "against Whisper, highlighting significant gains in multilingual accuracy and hallucination reduction. "
            "They also demonstrate LeMUR for conversational querying and structured intelligence extraction directly from audio transcripts."
        )

        self.utterances: List[MockUtterance] = [
            MockUtterance("A", "Welcome back to the podcast! Today we are thrilled to talk about speech AI architectures.", 0, 4800),
            MockUtterance("B", "Thanks for having me! It has been an incredible year for speech recognition and language modeling.", 5200, 11000),
            MockUtterance("A", "Could you walk us through the major challenges audio models faced in previous generations?", 11500, 17200),
            MockUtterance("B", "Historically, hallucination during pauses and background noise was a huge issue for transformer baselines.", 17800, 25000),
            MockUtterance("B", "With architectures like Universal-1, hallucination rates dropped by over thirty percent.", 25500, 32000),
            MockUtterance("A", "That is a massive improvement, especially for production audio intelligence pipelines.", 32500, 38000),
            MockUtterance("A", "What about natural language interaction using frameworks like LeMUR?", 38500, 43500),
            MockUtterance("B", "LeMUR allows developers to query transcripts directly, extracting action items and summaries effortlessly.", 44000, 52000),
            MockUtterance("A", "Thank you for sharing these insights with our listeners!", 52500, 56000),
            MockUtterance("B", "My pleasure! Excited to see what developers build with these tools.", 56500, 61000)
        ]

        self.sentiment_analysis: List[MockSentiment] = [
            MockSentiment("A", "Welcome back to the podcast! Today we are thrilled to talk about speech AI architectures.", "POSITIVE", 0, 4800),
            MockSentiment("B", "Thanks for having me! It has been an incredible year for speech recognition and language modeling.", "POSITIVE", 5200, 11000),
            MockSentiment("A", "Could you walk us through the major challenges audio models faced in previous generations?", "NEUTRAL", 11500, 17200),
            MockSentiment("B", "Historically, hallucination during pauses and background noise was a huge issue for transformer baselines.", "NEGATIVE", 17800, 25000),
            MockSentiment("B", "With architectures like Universal-1, hallucination rates dropped by over thirty percent.", "POSITIVE", 25500, 32000),
            MockSentiment("A", "That is a massive improvement, especially for production audio intelligence pipelines.", "POSITIVE", 32500, 38000),
            MockSentiment("A", "What about natural language interaction using frameworks like LeMUR?", "NEUTRAL", 38500, 43500),
            MockSentiment("B", "LeMUR allows developers to query transcripts directly, extracting action items and summaries effortlessly.", "POSITIVE", 44000, 52000),
            MockSentiment("A", "Thank you for sharing these insights with our listeners!", "POSITIVE", 52500, 56000),
            MockSentiment("B", "My pleasure! Excited to see what developers build with these tools.", "POSITIVE", 56500, 61000)
        ]

        self.iab_categories = MockIABCategories(
            summary={
                "Technology & Computing>Artificial Intelligence": 0.94,
                "Technology & Computing>Software>Audio & Video Software": 0.88,
                "Science>Computer Science": 0.82,
                "Education>Educational Technology": 0.65,
                "Business & Finance>Developer Tools": 0.61
            }
        )

        self.lemur = MockLemur(self)

    def get_sentences(self) -> List[MockSentence]:
        return [
            MockSentence(u.text, u.start, u.end, u.speaker)
            for u in self.utterances
        ]

def get_sample_transcript() -> MockTranscript:
    """Return pre-computed mock transcript for podcast.mp3 demo."""
    return MockTranscript()
