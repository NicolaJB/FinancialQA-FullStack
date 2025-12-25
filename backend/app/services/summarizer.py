# backend/app/services/summarizer.py
from transformers import pipeline as hf_pipeline

_summarizer = None

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = hf_pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            device=-1  # CPU
        )
        print("CPU-friendly summarizer loaded.")
    return _summarizer


def cpu_summarize(text: str, max_length: int = 130, min_length: int = 40) -> str:
    summarizer = get_summarizer()
    if not text.strip():
        return ""
    result = summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )
    return result[0]["summary_text"]
