import requests
import time
import json

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_ID = 101  # TDS category

def get_topics():
    url = f"{BASE_URL}/c/tds/{CATEGORY_ID}/l/latest.json"
    res = requests.get(url)
    if res.status_code != 200:
        print("Failed to get topics!")
        return []

    data = res.json()
    topics = data.get("topic_list", {}).get("topics", [])
    return topics

def get_posts(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Failed to get posts for topic {topic_id}")
        return []

    data = res.json()
    posts = data.get("post_stream", {}).get("posts", [])
    post_contents = []
    for post in posts:
        post_contents.append({
            "post_number": post["post_number"],
            "content": post["cooked"],
            "created_at": post["created_at"]
        })
    return post_contents

def scrape():
    all_data = []
    topics = get_topics()

    for topic in topics:
        topic_id = topic["id"]
        title = topic["title"]
        print(f"Scraping topic: {title}")
        posts = get_posts(topic_id)

        all_data.append({
            "topic_id": topic_id,
            "title": title,
            "posts": posts
        })

        time.sleep(1)  # Be polite to server

    # Save to file
    with open("discourse_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print("✅ Scraping complete. Data saved to discourse_data.json")

if __name__ == "__main__":
    scrape()
