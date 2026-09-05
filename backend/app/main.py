import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.base import Base
from app.database.connection import engine


from app.models.topic import Topic
from app.models.tag import Tag
from app.models.article import Article
from app.models.user import User
from app.models.article_tag import article_tags

from app.routes import topic, tag, article, timeline, search, ai, auth


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ChronoFlow API",
    description="AI-powered interactive timeline platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to ChronoFlow API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


app.include_router(auth.router)
app.include_router(topic.router)
app.include_router(tag.router)
app.include_router(article.router)
app.include_router(timeline.router)
app.include_router(search.router)
app.include_router(ai.router)