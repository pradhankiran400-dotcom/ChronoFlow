from datetime import date
from typing import Optional

from pydantic import BaseModel


# Create Article
class ArticleCreate(BaseModel):
    title: str
    summary: Optional[str] = None
    content: str
    event_date: date
    source_url: Optional[str] = None
    topic_id: int


# Update Article
class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    event_date: Optional[date] = None
    source_url: Optional[str] = None
    topic_id: Optional[int] = None


# Response
class ArticleResponse(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    content: str
    event_date: date
    source_url: Optional[str] = None
    topic_id: int

    class Config:
        from_attributes = True