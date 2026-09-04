from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.article import Article
from app.models.topic import Topic
from app.schemas.article import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse
)


router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)


# CREATE ARTICLE
@router.post(
    "",
    response_model=ArticleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db)
):
    # Check if topic exists
    topic = (
        db.query(Topic)
        .filter(Topic.id == article.topic_id)
        .first()
    )

    if not topic:
        raise HTTPException(
            status_code=404,
            detail="Topic not found"
        )

    new_article = Article(
        title=article.title,
        summary=article.summary,
        content=article.content,
        event_date=article.event_date,
        source_url=article.source_url,
        topic_id=article.topic_id
    )

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


# GET ALL ARTICLES
@router.get(
    "",
    response_model=list[ArticleResponse]
)
def get_articles(
    db: Session = Depends(get_db)
):
    return (
        db.query(Article)
        .order_by(Article.event_date)
        .all()
    )


# GET SINGLE ARTICLE
@router.get(
    "/{article_id}",
    response_model=ArticleResponse
)
def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    article = (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    return article


# UPDATE ARTICLE
@router.put(
    "/{article_id}",
    response_model=ArticleResponse
)
def update_article(
    article_id: int,
    updated_article: ArticleUpdate,
    db: Session = Depends(get_db)
):
    article = (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    # If topic_id is being changed, check the new topic
    if updated_article.topic_id is not None:

        topic = (
            db.query(Topic)
            .filter(Topic.id == updated_article.topic_id)
            .first()
        )

        if not topic:
            raise HTTPException(
                status_code=404,
                detail="New topic not found"
            )

    # Only update fields sent by the user
    update_data = updated_article.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)

    return article


# DELETE ARTICLE
@router.delete(
    "/{article_id}"
)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    article = (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    db.delete(article)
    db.commit()

    return {
        "message": "Article deleted successfully"
    }