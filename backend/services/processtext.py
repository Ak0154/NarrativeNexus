import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import os
from datetime import datetime

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

def processedtext(i, o):
    with open(i, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    soup = BeautifulSoup(raw_text, 'html.parser')
    text = soup.get_text(separator=' ').lower()

    # --- Tokenization and cleaning ---
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    # --- Lemmatization ---
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]

    cleaned_text = ' '.join(lemmatized_tokens)

    # --- Output handling ---
    os.makedirs(o, exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_path = os.path.join(o, f"cleaned_{timestamp}.txt")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    return output_path, cleaned_text[:500]

def analyze_sentiment(text: str):
    """
    Perform sentiment analysis on the given text using NLTK's VADER.
    Returns a dict with 'label' and 'scores'.
    """
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    compound = scores.get('compound', 0.0)
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'
    return {"label": label, "scores": scores}

if __name__ == "__main__":
    i = "app/backend/text_process/test.txt"
    o = "app/backend/text_process/cleaned"
    output_path, preview = processedtext(i, o)
    print(preview)
