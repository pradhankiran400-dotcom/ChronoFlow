from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.article import Article
from app.models.topic import Topic
from app.models.tag import Tag
from app.schemas.article import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse
)



from app.services.live_news import live_news_service

router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)


# SYNC LIVE ARTICLES
@router.post(
    "/sync-live",
    response_model=list[ArticleResponse]
)
def sync_live_articles(
    topic_id: int,
    query: Optional[str] = None,
    max_results: int = 8,
    db: Session = Depends(get_db)
):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(
            status_code=404,
            detail="Topic not found"
        )

    synced = live_news_service.sync_live_articles(
        db=db,
        topic_id=topic_id,
        query=query,
        max_results=max_results
    )

    return synced



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

    # Fetch tags if tag_ids provided
    tags = []
    if article.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(article.tag_ids)).all()
        if len(tags) != len(set(article.tag_ids)):
            raise HTTPException(
                status_code=400,
                detail="One or more tag IDs are invalid"
            )

    new_article = Article(
        title=article.title,
        summary=article.summary,
        content=article.content,
        event_date=article.event_date,
        source_url=article.source_url,
        topic_id=article.topic_id,
        tags=tags
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
    topic_id: Optional[int] = None,
    db: Session = Depends(get_db)
):

    query = db.query(Article)
    if topic_id:
        query = query.filter(Article.topic_id == topic_id)

    return query.order_by(Article.event_date.asc()).all()


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

    # If tag_ids are provided, update tags relationship
    if updated_article.tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(updated_article.tag_ids)).all()
        if len(tags) != len(set(updated_article.tag_ids)):
            raise HTTPException(
                status_code=400,
                detail="One or more tag IDs are invalid"
            )
        article.tags = tags

    # Only update fields sent by the user (excluding tag_ids which we handled above)
    update_data = updated_article.model_dump(
        exclude_unset=True,
        exclude={"tag_ids"}
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