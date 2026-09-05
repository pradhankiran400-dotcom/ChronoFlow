from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.tag import TagResponse
from app.schemas.topic import TopicResponse


# Create Article
class ArticleCreate(BaseModel):
    title: str
    summary: Optional[str] = None
    content: str
    event_date: date
    source_url: Optional[str] = None
    topic_id: int
    tag_ids: Optional[list[int]] = []


# Update Article
class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    event_date: Optional[date] = None
    source_url: Optional[str] = None
    topic_id: Optional[int] = None
    tag_ids: Optional[list[int]] = None


# Response
class ArticleResponse(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    content: str
    event_date: date
    source_url: Optional[str] = None
    topic_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    topic: Optional[TopicResponse] = None
    tags: list[TagResponse] = []

    class Config:
        from_attributes = True