import json
import openai
import os
import time

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load processed data
with open("processed_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Function to generate embeddings (new SDK format)
def get_embedding(text, model="text-embedding-ada-002"):
    try:
        response = openai.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        print("Error:", e)
        return None

# Prepare data with embeddings
embedded_data = []

for item in data:
    content = item["content"]
    embedding = get_embedding(content)
    if embedding:
        embedded_data.append({
            "topic_id": item["topic_id"],
            "title": item["title"],
            "content": content,
            "embedding": embedding
        })
        print(f"✅ Embedded topic: {item['title']}")
        time.sleep(1)  # Respect API limits

# Save embedded data
with open("embedded_data.json", "w", encoding="utf-8") as f:
    json.dump(embedded_data, f, indent=2)

print("✅ All embeddings generated and saved to embedded_data.json")
