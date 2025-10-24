from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.processtext import processedtext
from backend.services.model import summarize_text
import os
import shutil
import tempfile

router = APIRouter(prefix="/text", tags=["Text Processing"])

@router.post("/clean-and-summarize")
async def clean_and_summarize(file: UploadFile = File(...)):
    """
    Upload a text or HTML file.
    Cleans it using the NLTK + BeautifulSoup pipeline,
    then summarizes the cleaned text using a transformer model.
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            temp_path = tmp.name
            shutil.copyfileobj(file.file, tmp)

        output_dir = "app/backend/text_process/cleaned"
        output_path, preview = processedtext(temp_path, output_dir)

        # Read cleaned full text for summarization
        with open(output_path, 'r', encoding='utf-8') as f:
            cleaned_text = f.read()

        summary = summarize_text(cleaned_text)

        # Clean up temp file
        os.remove(temp_path)

        return {
            "message": "File cleaned and summarized successfully!",
            "output_file": output_path,
            "preview": preview,
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
