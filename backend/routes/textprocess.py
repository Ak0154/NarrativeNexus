from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile, shutil, os
from backend.services.processtext import processedtext  
from transformers import pipeline

# Initialize router
router = APIRouter()

# Load models globally (only once)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_analyzer = pipeline("sentiment-analysis")


def summarize_text(text: str, max_length: int = 150, min_length: int = 40) -> str:
    """
    Summarizes input text using a transformer model with dynamic length control.
    Automatically shortens max_length for smaller inputs to prevent warnings.
    """
    if not text.strip():
        return "No text provided for summarization."

    # Truncate input to prevent overflow for the model
    truncated_text = text[:3000]

    # Dynamically adjust max/min length based on input size
    input_length = len(truncated_text.split())
    if input_length < 100:
        # For very short text, reduce summary length
        max_length = min(60, int(input_length * 0.9))
        min_length = max(20, int(max_length * 0.5))
    elif input_length < 300:
        # For medium text
        max_length = min(120, int(input_length * 0.7))
        min_length = max(40, int(max_length * 0.5))
    else:
        # For longer inputs, keep defaults
        max_length = min(max_length, 150)
        min_length = max(min_length, 40)

    # Generate the summary
    summary = summarizer(
        truncated_text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )[0]['summary_text']

    return summary.strip()



def analyze_sentiment(text: str) -> dict:
    if not text.strip():
        return {"error": "No text provided for sentiment analysis."}

    result = sentiment_analyzer(text[:512])[0]
    return {
        "label": result['label'],
        "score": round(result['score'], 3)
    }


@router.post("/clean-and-summarize")
async def clean_and_summarize(file: UploadFile = File(...)):
    """
    Upload a text or HTML file.
    Cleans it using NLTK + BeautifulSoup,
    summarizes the cleaned text,
    and performs sentiment analysis on the summary.
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            temp_path = tmp.name
            shutil.copyfileobj(file.file, tmp)

        output_dir = "app/backend/text_process/cleaned"
        output_path, preview = processedtext(temp_path, output_dir)

        # Read cleaned text for summarization
        with open(output_path, 'r', encoding='utf-8') as f:
            cleaned_text = f.read()

        summary = summarize_text(cleaned_text)
        sentiment = analyze_sentiment(summary)

        # Clean up temp file
        os.remove(temp_path)

        return {
            "message": "File cleaned, summarized, and analyzed successfully!",
            "output_file": output_path,
            "preview": preview,
            "summary": summary,
            "sentiment": sentiment
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
