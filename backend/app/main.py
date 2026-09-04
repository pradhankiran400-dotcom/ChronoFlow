from fastapi import FastAPI
from app.database.base import Base
from app.database.connection import engine
from app.models.topic import Topic
from app.routes import topic

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.title = "ChronoFlow API"

@app.get("/")
def home():
    return {
        "message": "Welcome to the ChronoFlow API!"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

app.include_router(topic.router)