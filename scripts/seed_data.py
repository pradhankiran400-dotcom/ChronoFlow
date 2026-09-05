"""Seed sample ChronoFlow data through the API or TestClient."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "backend") not in sys.path:
    sys.path.append(str(PROJECT_ROOT / "backend"))

TOPICS = [
    {
        "name": "Artificial Intelligence",
        "description": "Important developments in artificial intelligence.",
    },
    {
        "name": "Space Exploration",
        "description": "Milestones in human and robotic spaceflight.",
    },
    {
        "name": "Climate & Environment",
        "description": "Global developments in climate science and sustainability.",
    },
]

TAGS = ["AI", "LLM", "Technology", "Space", "Climate", "Policy"]

ARTICLES = [
    {
        "title": "Launch of ChatGPT",
        "summary": "ChatGPT was released for public use.",
        "content": "ChatGPT introduced a conversational interface powered by large language models to a wide public audience in November 2022.",
        "source_url": "https://openai.com/blog/chatgpt",
        "event_date": "2022-11-30",
        "topic_name": "Artificial Intelligence",
        "tags": ["AI", "LLM", "Technology"],
    },
    {
        "title": "GPT-4 Release",
        "summary": "GPT-4 advanced large language models with stronger reasoning.",
        "content": "GPT-4 demonstrated improved reasoning and multimodal capabilities compared with earlier systems in March 2023.",
        "source_url": "https://openai.com/research/gpt-4",
        "event_date": "2023-03-14",
        "topic_name": "Artificial Intelligence",
        "tags": ["AI", "LLM", "Technology"],
    },
    {
        "title": "Growth of Generative AI",
        "summary": "Generative models moved from research into everyday tools.",
        "content": "During 2023, generative AI saw rapid adoption across writing, coding, design, and education.",
        "source_url": "https://example.com/genai",
        "event_date": "2023-07-01",
        "topic_name": "Artificial Intelligence",
        "tags": ["AI", "Technology"],
    },
    {
        "title": "James Webb First Images",
        "summary": "JWST released its first full-color images.",
        "content": "The James Webb Space Telescope delivered deep-field and nebula images that reshaped public and scientific views of the early universe.",
        "source_url": "https://nasa.gov/webbfirstimages",
        "event_date": "2022-07-12",
        "topic_name": "Space Exploration",
        "tags": ["Space", "Technology"],
    },
    {
        "title": "Artemis I Launch",
        "summary": "NASA's uncrewed lunar test flight succeeded.",
        "content": "The Space Launch System rocket sent the Orion spacecraft around the Moon, proving hardware readiness for deep space exploration.",
        "source_url": "https://nasa.gov/artemis-1",
        "event_date": "2022-11-16",
        "topic_name": "Space Exploration",
        "tags": ["Space", "Technology"],
    },
]


def main():
    from app.main import app
    from fastapi.testclient import TestClient

    client = TestClient(app)

    # 1. Topics
    topics_res = client.get("/topics/")
    existing_topics = {t["name"]: t for t in topics_res.json()}
    for topic in TOPICS:
        if topic["name"] not in existing_topics:
            res = client.post("/topics/", json=topic)
            existing_topics[res.json()["name"]] = res.json()
            print("Created topic:", topic["name"])

    # 2. Tags
    tags_res = client.get("/tags")
    existing_tags = {tag["name"]: tag for tag in tags_res.json()}
    for name in TAGS:
        if name not in existing_tags:
            res = client.post("/tags", json={"name": name})
            existing_tags[name] = res.json()
            print("Created tag:", name)

    # 3. Articles
    articles_res = client.get("/articles")
    existing_titles = {a["title"] for a in articles_res.json()}
    for article in ARTICLES:
        if article["title"] in existing_titles:
            continue
        tag_ids = [existing_tags[name]["id"] for name in article.get("tags", []) if name in existing_tags]
        payload = {
            "title": article["title"],
            "summary": article["summary"],
            "content": article["content"],
            "source_url": article["source_url"],
            "event_date": article["event_date"],
            "topic_id": existing_topics[article["topic_name"]]["id"],
            "tag_ids": tag_ids,
        }
        res = client.post("/articles", json=payload)
        if res.status_code == 201:
            print("Created article:", article["title"])
        else:
            print("Error creating article:", article["title"], res.text)


if __name__ == "__main__":
    main()

