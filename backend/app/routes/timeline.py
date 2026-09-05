from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.article import Article
from app.models.topic import Topic
from app.models.tag import Tag
from app.schemas.timeline import TimelineResponse
from app.schemas.topic import TopicResponse

router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"]
)


@router.get("", response_model=TimelineResponse)
def get_timeline(
    topic_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    tag_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Article)

    selected_topic = None
    if topic_id:
        selected_topic = db.query(Topic).filter(Topic.id == topic_id).first()
        query = query.filter(Article.topic_id == topic_id)

    if start_date:
        query = query.filter(Article.event_date >= start_date)

    if end_date:
        query = query.filter(Article.event_date <= end_date)

    if tag_id:
        query = query.filter(Article.tags.any(Tag.id == tag_id))

    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            (Article.title.ilike(search_pattern)) |
            (Article.summary.ilike(search_pattern)) |
            (Article.content.ilike(search_pattern))
        )

    events = query.order_by(Article.event_date.asc()).all()

    topic_response = TopicResponse.model_validate(selected_topic) if selected_topic else None

    return {
        "topic": topic_response,
        "events": events
    }
