from pathlib import Path
import sys

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session


# Add project root to Python path
PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[3]
)

sys.path.append(
    str(PROJECT_ROOT / "ai_ml")
)


from rag.pipeline import RAGPipeline

from app.database.connection import get_db
from app.models.article import Article


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class QuestionRequest(BaseModel):

    question: str


rag_pipeline = RAGPipeline()


@router.post("/ask")
def ask_ai(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):

    articles = db.query(Article).all()

    article_data = []

    for article in articles:

        article_data.append(
            {
                "id": article.id,
                "title": article.title,
                "summary": article.summary,
                "content": article.content
            }
        )

    result = rag_pipeline.ask(
        question=request.question,
        articles=article_data
    )

    return result