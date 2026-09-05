from typing import Optional
from pydantic import BaseModel
from app.schemas.topic import TopicResponse
from app.schemas.article import ArticleResponse


class TimelineResponse(BaseModel):
    topic: Optional[TopicResponse] = None
    events: list[ArticleResponse]

    class Config:
        from_attributes = True
