# Audio Analysis App using AssemblyAI API

This project demonstrates how to build a comprehensive audio analysis application using the [AssemblyAI API](https://www.assemblyai.com/) and [Streamlit](https://streamlit.io/) for the web interface. The app allows you to upload an audio file and performs the following tasks:

1. **Transcribes the audio**.
2. **Performs sentiment analysis on the audio**.
3. **Summarizes the audio**.
4. **Identifies named entities mentioned in the audio**.
5. **Extracts broad ideas from the audio**.
6. **Enables interaction with the audio in natural language** using AssemblyAI's LeMUR framework.

## Features

- **Audio Transcription**: Transcribes the provided audio file into text.
- **Sentiment Analysis**: Analyzes the sentiment of each sentence in the transcript.
- **Audio Summarization**: Generates a summary of the audio content.
- **Named Entity Recognition (NER)**: Identifies and extracts entities mentioned in the audio.
- **Broad Ideas Extraction**: Detects and displays topics using IAB categories.
- **Natural Language Interaction**: Allows the user to interact with the audio transcript using AssemblyAI's LeMUR framework.

Enable features like speaker labels, summarization, and sentiment analysis by configuring the `TranscriptionConfig` object:

```python
config = aai.TranscriptionConfig(
    speaker_labels=True,
    iab_categories=True,
    sentiment_analysis=True,
    summarization=True,
    language_detection=True
)
```

## App Workflow

1. The user uploads an audio file.
2. The audio file is sent to AssemblyAI for transcription and additional analyses such as sentiment analysis, language identification, summarization, etc.
3. The transcript is returned, and the results are displayed in the app.
4. The user can interact with the transcript using natural language to extract more insights, ask questions, and interact with the content using AssemblyAI's LeMUR.

### Step-by-Step Implementation:

1. **Import Required Packages**:
    ```python
    import assemblyai as aai
    import streamlit as st
    ```
   
2. **Set Your API Key**:
    ```python
    aai.settings.api_key = 'your_assemblyai_api_key'
    ```

3. **File Upload**:
    Use a Streamlit file uploader widget to allow the user to upload the audio file:
    ```python
    audio_file = st.file_uploader("Upload your audio file", type=["wav", "mp3"])
    ```

4. **Transcription Process**:
    Once the file is uploaded, send it for transcription:
    ```python
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    ```

5. **Enabling Additional Insights**:
    In the `TranscriptionConfig` object, enable features like speaker labels, sentiment analysis, and topic extraction:
    ```python
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        iab_categories=True,
        sentiment_analysis=True,
        summarization=True,
        language_detection=True
    )
    transcript = transcriber.transcribe(audio_file, config)
    ```

6. **Displaying the Results**:
    - **Transcription Summary**: 
        ```python
        st.write(transcript.summary)
        ```
    - **Sentence-Level Transcription**:
        Use the `get_sentences()` method to display sentence-level transcriptions:
        ```python
        for sentence in transcript.get_sentences():
            st.write(sentence.text)
        ```
    - **Speaker Labels**: 
        You can print speaker labels alongside the transcript:
        ```python
        for sentence in transcript.get_sentences():
            st.write(f"Speaker {sentence.speaker}: {sentence.text}")
        ```
    - **Sentiment Analysis**: 
        Display sentiment analysis using Streamlit's warning, success, and error boxes:
        ```python
        for sentence in transcript.get_sentences():
            sentiment = sentence.sentiment
            st.write(f"Sentiment: {sentiment}")
        ```
    - **Topic Detection (IAB Categories)**: 
        Display the broad topics detected:
        ```python
        st.write(transcript.iab_categories)
        ```

7. **Natural Language Interaction with LeMUR**:
    Use AssemblyAI’s LeMUR framework to interact with the transcript in natural language:
    ```python
    prompt = st.text_input("Ask a question about the audio")
    if prompt:
        response = transcript.lemur(prompt)
        st.write(response)
    ```

## Running the Application

To run the application, execute the following:

```bash
streamlit run app.py
```

This will open the Streamlit web interface in your browser, where you can upload an audio file and see the results of the transcription, sentiment analysis, entity recognition, topic extraction, and interact with the audio through natural language.

## A Departing Note

I first used AssemblyAI two years ago, and in my experience, it has the most developer-friendly and intuitive SDKs to integrate speech AI into applications.

Earlier this year, AssemblyAI released Universal-1, a state-of-the-art multimodal speech recognition model trained on 12.5 million hours of multilingual audio data. It improves transcription accuracy and reduces hallucination rates while supporting multiple languages.

### Universal-1 Model Highlights:

- **10% or greater accuracy improvement** in English, Spanish, and German.
- **30% lower hallucination rate** than OpenAI Whisper Large-v3.
- Supports **multiple languages within a single audio file**.

## Prerequisites

To run this app, you will need:

- A free [AssemblyAI API key](https://www.assemblyai.com/), which provides $50 worth of free transcription credits.
- Python installed on your machine.
- [Streamlit](https://docs.streamlit.io/) for building the web interface.

### Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   ```

2. Install the required Python packages:

   ```bash
   pip install assemblyai streamlit
   ```

3. Set your AssemblyAI API key in the environment:

   ```python
   api_key = 'your_assemblyai_api_key'
   ```

4. Run the application:

   ```bash
   streamlit run app.py
   ```

Thanks for following!