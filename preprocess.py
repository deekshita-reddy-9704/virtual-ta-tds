import json
import nltk
from bs4 import BeautifulSoup

# Function to clean HTML content
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

# Function to load discourse data
def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# Preprocessing function
def preprocess():
    data = load_data("discourse_data.json")
    documents = []

    for topic in data:
        for post in topic["posts"]:
            text = clean_html(post["content"])
            documents.append({
                "topic_id": topic["topic_id"],
                "title": topic["title"],
                "content": text
            })

    # Save processed data
    with open("processed_data.json", "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)

    print("✅ Preprocessing complete. Saved to processed_data.json")

if __name__ == "__main__":
    preprocess()
