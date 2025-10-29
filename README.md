# 🧠Narrative Nexus

A simple yet powerful web app built with **FastAPI + Transformers + Vanilla JS** that lets you:

- 🧹 Clean raw text or HTML content (using NLTK + BeautifulSoup)
- ✂️ Summarize the cleaned text using `facebook/bart-large-cnn`
- 💬 Analyze the **sentiment** (Positive / Negative / Neutral) of the generated summary

All in one neat, minimal dark-themed interface.

---

## 🚀 Features

- **Drag & Drop Uploads** — upload `.txt` or `.html` files directly  
- **Instant Cleaning** — removes HTML tags, scripts, and unwanted formatting  
- **AI-Powered Summarization** — compresses long text into key insights  
- **Sentiment Analysis** — interprets the emotional tone of the text  
- **FastAPI Backend** — lightweight and async  
- **Vanilla JS Frontend** — no frameworks, just clean HTML + JS  
- **Offline-ready** — supports loading models locally to avoid re-downloads  

---

## 🧩 Project Structure

```

.
├── nexusnarrative/
│   ├── backend/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── routes/
│   │   │   └── text_routes.py   # /clean-and-summarize endpoint
│   │   ├── text_process/
│   │   │   ├── cleaner.py       # Uses NLTK + BeautifulSoup
│   │   │   └── cleaned/         # Output directory
│   └── models/                  # (optional) local cached transformers models
│
├── frontend/
│   └── index.html               # Minimal UI
│
└── requirements.txt

````

---

## ⚙️ Backend Setup (FastAPI)

### 1️⃣ Create and activate a virtual environment
```bash
uv venv(intstall uv using pip install uv)

source .venv/bin/activate     # on Windows: .venv\Scripts\activate
````

### 2️⃣ Install dependencies

```bash
puv add uvicorn transformers torch beautifulsoup4 nltk
```

> The first time you run the app, Hugging Face will download model weights (`model.safetensors`).
> These are cached locally and won’t re-download later.

### 3️⃣ Run the backend

```bash
uvicorn main:app --reload
```

The API should now be live at:

```
http://127.0.0.1:8000
```

Example endpoint:

```
POST /text/clean-and-summarize
```

It accepts a file upload (`.txt` or `.html`) and returns:

```json
{
  "message": "File cleaned, summarized, and analyzed successfully!",
  "preview": "First 500 chars...",
  "summary": "AI-generated summary text...",
  "sentiment": {
    "label": "POSITIVE",
    "score": 0.987
  }
}
```

---

## 💻 Frontend Setup

1. Open `frontend/index.html` in your browser.
2. Make sure the API base URL in the file points to your FastAPI server:

   ```html
   <code id="api-url">http://127.0.0.1:8000</code>
   ```
3. Upload or paste some text — and hit **“Clean, Summarize & Analyze”**.

---

## 🧠 How It Works

1. Uploaded text is cleaned with **NLTK** and **BeautifulSoup**
2. Cleaned text is summarized by **BART (facebook/bart-large-cnn)**
3. The summary is analyzed using **DistilBERT sentiment model**
4. The response includes:

   * Cleaned preview
   * Summarized text
   * Sentiment label + confidence score

The frontend displays all of these neatly in separate panels.

---

## 🗂 Example Output

```
Input: 3-page HTML article about global warming
→ Cleaned: 4,500 words
→ Summary: “Global emissions continue to rise as countries struggle to meet Paris targets...”
→ Sentiment: NEGATIVE (confidence: 98.7%)
```

---

## 🧰 Optional: Local Model Storage (Offline Mode)

If you don’t want the app to download models every time:

```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

model_name = "facebook/bart-large-cnn"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir="./app/models")
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir="./app/models")

summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
```

Then add:
uv add "beautifulsoup4>=4.14.2" "fastapi>=0.120.0" "nltk>=3.9.2" "python-multipart>=0.0.20" "torch>=2.9.0" "transformers>=4.57.1" "uvicorn>=0.38.0" "huggingface-hub>=0.26.2"

```bash
export TRANSFORMERS_OFFLINE=1
```

---

## 🧑‍💻 Developer Notes

* Summarization input is truncated to **3000 chars** to fit model limits
* Sentiment input limited to **512 tokens** for performance
* Backend cleans up temporary files automatically
* Works smoothly with async FastAPI routes

---

## 🏁 Future Ideas

* [ ] Add translation support
* [ ] Multi-language sentiment detection
* [ ] Option to export cleaned + summarized text as `.txt`
* [ ] Docker support for easy deployment

---

## 🧡 Credits

Built with:

* [FastAPI](https://fastapi.tiangolo.com/)
* [Hugging Face Transformers](https://huggingface.co/transformers/)
* [NLTK](https://www.nltk.org/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

> Created by Akash Kumar
(krakash2031@gmail.com)