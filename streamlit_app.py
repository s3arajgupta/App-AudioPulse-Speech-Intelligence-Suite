"""AudioPulse: All-in-One Speech Intelligence & Audio Analysis Suite.

Production Streamlit application leveraging AssemblyAI Universal-1 and LeMUR LLM
to extract transcription, speaker diarization, sentence sentiment, IAB taxonomies,
and conversational reasoning from speech.
"""

import os
import io
import json
import streamlit as st
from pathlib import Path

from src.audiopulse.config import AudioPulseConfig, get_api_key
from src.audiopulse.transcriber import (
    transcribe_audio,
    timestamp_string,
    calculate_sentiment_stats,
)
from src.audiopulse.lemur_agent import query_lemur
from src.audiopulse.exporter import transcript_to_dict, generate_markdown_report
from src.audiopulse.mock_data import get_sample_transcript

# Streamlit Page Config
st.set_page_config(
    page_title="AudioPulse — Speech Intelligence Suite",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for rich styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }
    .badge-speaker-a {
        background-color: #e0e7ff;
        color: #3730a3;
    }
    .badge-speaker-b {
        background-color: #fce7f3;
        color: #9d174d;
    }
    .badge-pos {
        background-color: #dcfce7;
        color: #166534;
    }
    .badge-neu {
        background-color: #f1f5f9;
        color: #475569;
    }
    .badge-neg {
        background-color: #fee2e2;
        color: #991b1b;
    }
    .dialogue-box {
        border-left: 3px solid #6366f1;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.6rem;
        background-color: #fafafa;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None
if "audio_filename" not in st.session_state:
    st.session_state.audio_filename = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def load_sample_podcast():
    """Load local podcast.mp3 and sample intelligence dataset."""
    sample_path = Path(__file__).parent / "podcast.mp3"
    if sample_path.exists():
        with open(sample_path, "rb") as f:
            st.session_state.audio_bytes = f.read()
        st.session_state.audio_filename = "podcast.mp3 (Sample)"
    else:
        st.session_state.audio_filename = "podcast.mp3 (Demo)"

    st.session_state.transcript = get_sample_transcript()
    st.session_state.chat_history = [
        {"role": "assistant", "content": "I am your LeMUR audio assistant. Ask me anything about this conversation!"}
    ]


def main():
    # Sidebar: Configurations and File Uploads
    with st.sidebar:
        st.header("⚙️ Settings & Controls")

        api_key_env = get_api_key()
        api_key_input = st.text_input(
            "AssemblyAI API Key",
            type="password",
            value=api_key_env,
            help="Get your free key at assemblyai.com. Not required for One-Click Demo.",
        )

        st.markdown("---")
        st.subheader("Model Configuration")
        speakers_expected = st.slider("Expected Speakers", min_value=1, max_value=8, value=2)
        enable_diarization = st.checkbox("Speaker Diarization", value=True)
        enable_sentiment = st.checkbox("Sentiment Analysis", value=True)
        enable_topics = st.checkbox("IAB Topic Categorization", value=True)
        enable_summary = st.checkbox("Abstractive Summary", value=True)

        st.markdown("---")
        st.subheader("⚡ Quick Start")
        if st.button("🚀 Load Sample Podcast (One-Click Demo)", use_container_width=True):
            load_sample_podcast()
            st.success("Sample podcast loaded instantly!")

        st.markdown("---")
        st.subheader("📁 Upload Your Audio")
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=["mp3", "wav", "m4a", "aac", "ogg", "flac"],
            help="Upload meeting recordings, podcasts, or customer calls.",
        )

        if uploaded_file is not None and (
            st.session_state.audio_filename != uploaded_file.name
        ):
            st.session_state.audio_bytes = uploaded_file.getvalue()
            st.session_state.audio_filename = uploaded_file.name

            config = AudioPulseConfig(
                api_key=api_key_input,
                speakers_expected=speakers_expected,
                speaker_labels=enable_diarization,
                sentiment_analysis=enable_sentiment,
                iab_categories=enable_topics,
                summarization=enable_summary,
            )

            with st.spinner("Transcribing and analyzing with AssemblyAI Universal-1..."):
                transcript = transcribe_audio(
                    uploaded_file,
                    config=config,
                    api_key=api_key_input,
                    force_mock=(not bool(api_key_input)),
                )
                st.session_state.transcript = transcript
                st.session_state.chat_history = [
                    {"role": "assistant", "content": "I am your LeMUR audio assistant. Ask me anything about this conversation!"}
                ]
                st.success(f"Analysis complete for {uploaded_file.name}!")

    # Main Header
    st.markdown('<div class="main-title">AudioPulse 🎙️</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">All-in-One Speech Intelligence & Audio Analytics powered by AssemblyAI Universal-1 & LeMUR</div>',
        unsafe_allow_html=True,
    )

    # Empty State Warning
    if st.session_state.transcript is None:
        st.info(
            "👋 Welcome! Click **'Load Sample Podcast (One-Click Demo)'** in the sidebar to test immediately, "
            "or upload your own audio file with an AssemblyAI API key."
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🎯 Core Capabilities")
            st.write("- 🗣️ **Universal-1 ASR** speech-to-text")
            st.write("- 👥 **Speaker Diarization** timeline")
            st.write("- 📈 **Sentence Sentiment** quantification")
        with col2:
            st.markdown("### 🏷️ Content Intelligence")
            st.write("- 🗂️ **IAB 3-Tier Taxonomy** categorization")
            st.write("- 📋 **Abstractive Summarization**")
            st.write("- 📄 **Multi-Format Exports** (JSON, MD, TXT)")
        with col3:
            st.markdown("### 🧠 LeMUR Reasoning")
            st.write("- 💬 **Conversational Audio Q&A**")
            st.write("- 📌 **Action Item & Insight Extraction**")
            st.write("- ⚡ **Zero-Setup Demo** included")
        return

    transcript = st.session_state.transcript

    # Audio Player & Quick Metrics
    st.subheader(f"Audio Source: `{st.session_state.audio_filename}`")
    if st.session_state.audio_bytes:
        st.audio(st.session_state.audio_bytes)

    stats = calculate_sentiment_stats(transcript)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Duration", timestamp_string(getattr(transcript, "audio_duration", 0) * 1000))
    with m2:
        st.metric("Utterances", len(getattr(transcript, "utterances", [])))
    with m3:
        st.metric("Positive Sentiment", f"{stats['positive_pct']}%", delta=f"{stats['POSITIVE']} sentences")
    with m4:
        st.metric("Language", str(getattr(transcript, "language_code", "en_us")).upper())

    st.markdown("---")

    # 5 Rich Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Executive Summary",
        "👥 Speaker Diarization",
        "📊 Sentiment Analysis",
        "🏷️ IAB Topics",
        "🧠 LeMUR AI Copilot",
    ])

    # Tab 1: Executive Summary & Full Text
    with tab1:
        st.subheader("Executive Summary")
        summary_text = getattr(transcript, "summary", "Summary not available.")
        st.info(summary_text)

        st.subheader("Full Transcript")
        with st.expander("View Full Text", expanded=False):
            st.write(getattr(transcript, "text", ""))

        st.subheader("Sentence-by-Sentence Breakdown")
        sentences = []
        if hasattr(transcript, "get_sentences"):
            sentences = transcript.get_sentences()
        elif hasattr(transcript, "sentiment_analysis"):
            sentences = transcript.sentiment_analysis

        search_query = st.text_input("Filter transcript lines by keyword", placeholder="Type a keyword...")
        for s in sentences:
            s_text = getattr(s, "text", "")
            if search_query.lower() in s_text.lower():
                s_start = getattr(s, "start", 0)
                st.write(f"`{timestamp_string(s_start)}` {s_text}")

    # Tab 2: Speaker Diarization
    with tab2:
        st.subheader("Speaker Dialogue Timeline")
        utterances = getattr(transcript, "utterances", [])

        if not utterances:
            st.warning("No speaker utterances found. Ensure speaker labels are enabled.")
        else:
            speakers = sorted(list(set(getattr(u, "speaker", "Unknown") for u in utterances)))
            st.write(f"**Identified Speakers ({len(speakers)}):** " + ", ".join([f"`Speaker {s}`" for s in speakers]))

            for u in utterances:
                spk = getattr(u, "speaker", "A")
                text = getattr(u, "text", "")
                start_t = timestamp_string(getattr(u, "start", 0))
                end_t = timestamp_string(getattr(u, "end", 0))

                badge_class = "badge-speaker-a" if spk == "A" else "badge-speaker-b"
                st.markdown(
                    f'<div class="dialogue-box">'
                    f'<span class="badge {badge_class}">Speaker {spk}</span> '
                    f'<span style="color:#94a3b8; font-size:0.85rem;">[{start_t} → {end_t}]</span><br/>'
                    f'<span style="color:#1e293b;">{text}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # Tab 3: Sentiment Analysis
    with tab3:
        st.subheader("Sentiment Distribution")
        col_pos, col_neu, col_neg = st.columns(3)
        with col_pos:
            st.markdown(f"### 🟢 Positive: {stats['positive_pct']}%")
            st.progress(stats['positive_pct'] / 100.0)
            st.caption(f"{stats['POSITIVE']} positive statements")
        with col_neu:
            st.markdown(f"### ⚪ Neutral: {stats['neutral_pct']}%")
            st.progress(stats['neutral_pct'] / 100.0)
            st.caption(f"{stats['NEUTRAL']} neutral statements")
        with col_neg:
            st.markdown(f"### 🔴 Negative: {stats['negative_pct']}%")
            st.progress(stats['negative_pct'] / 100.0)
            st.caption(f"{stats['NEGATIVE']} negative statements")

        st.markdown("---")
        st.subheader("Annotated Sentiments")

        sentiment_filter = st.selectbox("Filter by sentiment", ["All", "POSITIVE", "NEUTRAL", "NEGATIVE"])
        sentiments = getattr(transcript, "sentiment_analysis", [])

        for s in sentiments:
            sent_val = getattr(s, "sentiment", "NEUTRAL")
            if sentiment_filter != "All" and sent_val != sentiment_filter:
                continue

            speaker = getattr(s, "speaker", "A")
            start_t = timestamp_string(getattr(s, "start", 0))
            text = getattr(s, "text", "")

            if sent_val == "POSITIVE":
                st.success(f"`{start_t}` **[Speaker {speaker}]**: {text}")
            elif sent_val == "NEGATIVE":
                st.error(f"`{start_t}` **[Speaker {speaker}]**: {text}")
            else:
                st.info(f"`{start_t}` **[Speaker {speaker}]**: {text}")

    # Tab 4: IAB Content Categorization
    with tab4:
        st.subheader("IAB Content Taxonomy & Topic Relevance")
        iab_dict = {}
        if hasattr(transcript, "iab_categories") and hasattr(transcript.iab_categories, "summary"):
            iab_dict = dict(transcript.iab_categories.summary)

        if not iab_dict:
            st.warning("No IAB topic categories extracted for this transcript.")
        else:
            sorted_topics = sorted(iab_dict.items(), key=lambda x: x[1], reverse=True)
            for topic, score in sorted_topics:
                pct = round(score * 100, 1)
                st.write(f"**{topic}** (`{pct}%`)")
                st.progress(min(score, 1.0))

    # Tab 5: LeMUR AI Copilot
    with tab5:
        st.subheader("🧠 Conversational Audio Intelligence (LeMUR)")
        st.caption("Ask questions, generate meeting action items, or extract key insights using Claude 3.5 Sonnet over the transcript.")

        # Suggested quick questions
        st.write("**Suggested prompts:**")
        cq1, cq2, cq3 = st.columns(3)
        quick_prompt = None
        if cq1.button("📋 Key Takeaways"):
            quick_prompt = "Summarize the key takeaways and main discussion points."
        if cq2.button("👥 Speaker Dynamics"):
            quick_prompt = "What was the tone and relationship between Speaker A and Speaker B?"
        if cq3.button("🎯 Action Items"):
            quick_prompt = "Extract any decisions, recommendations, or action items mentioned in this audio."

        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_query = st.chat_input("Ask a question about this audio conversation...")
        prompt_to_run = user_query or quick_prompt

        if prompt_to_run:
            st.session_state.chat_history.append({"role": "user", "content": prompt_to_run})
            with st.chat_message("user"):
                st.write(prompt_to_run)

            with st.chat_message("assistant"):
                with st.spinner("LeMUR reasoning in progress..."):
                    answer = query_lemur(transcript, prompt_to_run)
                    st.write(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # Download Center
    st.markdown("---")
    st.subheader("📥 Export & Reports")
    d1, d2, d3 = st.columns(3)

    raw_text = getattr(transcript, "text", "")
    dict_data = transcript_to_dict(transcript)
    md_report = generate_markdown_report(transcript)

    with d1:
        st.download_button(
            "📄 Download Transcript (.txt)",
            data=raw_text,
            file_name=f"{st.session_state.audio_filename}_transcript.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            "📊 Download Analysis (.json)",
            data=json.dumps(dict_data, indent=2),
            file_name=f"{st.session_state.audio_filename}_analysis.json",
            mime="application/json",
            use_container_width=True,
        )
    with d3:
        st.download_button(
            "📑 Download Report (.md)",
            data=md_report,
            file_name=f"{st.session_state.audio_filename}_report.md",
            mime="text/markdown",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()