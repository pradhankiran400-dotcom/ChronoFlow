from fastapi import FastAPI

from app.database.base import Base
from app.database.connection import engine

from app.models.topic import Topic
from app.models.tag import Tag
from app.models.article import Article
from app.routes import ai

from app.routes import topic, tag, article


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ChronoFlow API",
    description="AI-powered interactive timeline platform",
    version="1.0.0"
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


app.include_router(topic.router)
app.include_router(tag.router)
app.include_router(article.router)
app.include_router(ai.router)