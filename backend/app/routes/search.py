from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.article import Article
from app.schemas.article import ArticleResponse

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.get("")
def search_articles(
    q: str = Query("", description="Search term"),
    topic_id: Optional[int] = Query(None, description="Optional topic filter"),
    db: Session = Depends(get_db)
):
    query_str = q.strip()
    if not query_str:
        return {
            "query": q,
            "results": []
        }

    pattern = f"%{query_str}%"
    db_query = db.query(Article).filter(
        (Article.title.ilike(pattern)) |
        (Article.summary.ilike(pattern)) |
        (Article.content.ilike(pattern))
    )

    if topic_id:
        db_query = db_query.filter(Article.topic_id == topic_id)

    results = db_query.order_by(Article.event_date.asc()).all()

    formatted_results = [
        ArticleResponse.model_validate(art) for art in results
    ]

    return {
        "query": q,
        "results": formatted_results
    }
