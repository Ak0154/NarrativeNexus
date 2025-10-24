from transformers import pipeline

# Load model once at startup
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str, max_length: int = 150, min_length: int = 40) -> str:
    """
    Summarizes input text using a transformer model.
    Automatically truncates overly long input to avoid model limits.
    """
    if not text.strip():
        return "No text provided for summarization."

    # Truncate input if it's too long for the model
    truncated_text = text[:3000]  

    summary = summarizer(
        truncated_text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )[0]['summary_text']

    return summary.strip()
