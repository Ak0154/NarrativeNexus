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
from transformers import pipeline

# Load models once at startup
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis")

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

def analyze_sentiment(text: str) -> dict:
    """
    Analyzes sentiment (positive, negative, or neutral) of the given text.
    Returns the label and confidence score.
    """
    if not text.strip():
        return {"error": "No text provided for sentiment analysis."}

    result = sentiment_analyzer(text[:512])[0]  # truncating for model input limit
    return {
        "label": result['label'],
        "score": round(result['score'], 3)
    }

def summarize_and_analyze(text: str) -> dict:
    """
    Combines summarization and sentiment analysis.
    Returns both the summary and the sentiment of the summary.
    """
    summary = summarize_text(text)
    sentiment = analyze_sentiment(summary)
    return {
        "summary": summary,
        "sentiment": sentiment
    }

# Example usage:
if __name__ == "__main__":
    sample_text = """
    The global climate crisis continues to worsen as greenhouse gas emissions reach record levels.
    Governments worldwide are struggling to meet the targets set by the Paris Agreement, while
    renewable energy adoption grows steadily but not fast enough to offset fossil fuel consumption.
    """
    
    result = summarize_and_analyze(sample_text)
    print("Summary:", result["summary"])
    print("Sentiment:", result["sentiment"])
