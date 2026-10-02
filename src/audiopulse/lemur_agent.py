"""LeMUR LLM Reasoning and Transcript Q&A Agent."""

from typing import Any

def query_lemur(transcript: Any, prompt: str, model_name: str = "claude3_5_sonnet") -> str:
    """Execute a natural language task on the transcript using AssemblyAI LeMUR."""
    if not prompt or not prompt.strip():
        return "Please enter a valid question or prompt."

    try:
        if hasattr(transcript, "lemur") and transcript.lemur is not None:
            import assemblyai as aai
            model_enum = getattr(aai.LemurModel, model_name, aai.LemurModel.claude3_5_sonnet)
            full_prompt = f"Based on the transcript, answer the following question: {prompt}"
            result = transcript.lemur.task(full_prompt, final_model=model_enum)
            return str(getattr(result, "response", result)).strip()
    except Exception as e:
        # Fallback to transcript mock lemur if available
        if hasattr(transcript, "lemur"):
            res = transcript.lemur.task(prompt)
            return getattr(res, "response", str(res))
        return f"LeMUR inquiry encountered an error: {e}"

    return "LeMUR is not available for this transcript."
