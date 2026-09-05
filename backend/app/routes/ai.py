from pathlib import Path
import sys
from typing import Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Add project root to Python path
PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[3]
)

if str(PROJECT_ROOT / "ai_ml") not in sys.path:
    sys.path.append(str(PROJECT_ROOT / "ai_ml"))

from rag.pipeline import RAGPipeline
from retrieval.search import Retriever
from app.database.connection import get_db
from app.models.article import Article

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class QuestionRequest(BaseModel):
    question: str
    topic_id: Optional[int] = None


rag_pipeline = RAGPipeline()
retriever = Retriever()


@router.post("/ask")
def ask_ai(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):
    query = db.query(Article)
    if request.topic_id:
        query = query.filter(Article.topic_id == request.topic_id)

    articles = query.all()

    article_data = []
    for article in articles:
        article_data.append(
            {
                "id": article.id,
                "title": article.title,
                "summary": article.summary,
                "content": article.content,
                "event_date": str(article.event_date),
                "source_url": article.source_url
            }
        )

    result = rag_pipeline.ask(
        question=request.question,
        articles=article_data
    )

    return result


@router.get("/search")
def semantic_search(
    q: str = Query("", description="Query for semantic vector search"),
    topic_id: Optional[int] = Query(None, description="Optional topic filter"),
    db: Session = Depends(get_db)
):
    query_str = q.strip()
    if not query_str:
        return {
            "query": q,
            "results": []
        }

    query = db.query(Article)
    if topic_id:
        query = query.filter(Article.topic_id == topic_id)

    articles = query.all()
    article_data = []
    for article in articles:
        article_data.append(
            {
                "id": article.id,
                "title": article.title,
                "summary": article.summary,
                "content": article.content,
                "event_date": str(article.event_date),
                "source_url": article.source_url,
                "topic_id": article.topic_id
            }
        )

    results = retriever.search(
        question=query_str,
        articles=article_data,
        top_k=10
    )

    return {
        "query": q,
        "results": results
    }