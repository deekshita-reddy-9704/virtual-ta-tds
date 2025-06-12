import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI  # ✅ correct import
import base64
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
# Setup Flask app
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Virtual TA API! Use the /api/ endpoint to send your questions."
    })

# Load embedded data
with open("embedded_data.json", "r", encoding="utf-8") as f:
    embedded_data = json.load(f)

# Load embeddings into numpy arrays
for item in embedded_data:
    item["embedding"] = np.array(item["embedding"])

# Load your OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to get embedding for question
def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return np.array(response.data[0].embedding)

# Function to compute cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# API endpoint
@app.route('/api/', methods=['POST'])
def answer_question():
    data = request.get_json()

    question = data.get("question", "")
    image_data = data.get("image", None)

    # Optional image handling (skipped for now)
    if image_data:
        print("Received image, but skipping image processing for now.")

    # Get embedding for question
    try:
        question_embedding = get_embedding(question)
    except Exception as e:
        return jsonify({"error": f"Embedding failed: {str(e)}"})

    # Find top 2 similar discourse posts
    similarities = []
    for item in embedded_data:
        score = cosine_similarity(question_embedding, item["embedding"])
        similarities.append((score, item))

    similarities.sort(reverse=True, key=lambda x: x[0])
    top_matches = similarities[:2]

    # Prepare mock answer
    answer = "Based on Discourse data, here's a helpful answer."

    # Prepare links
    links = []
    for score, item in top_matches:
        links.append({
            "url": f"https://discourse.onlinedegree.iitm.ac.in/t/{item['topic_id']}",
            "text": item['title']
        })

    response = {
        "answer": answer,
        "links": links
    }
    return jsonify(response)

# Run app locally
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
