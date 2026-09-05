from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    summary = Column(
        Text,
        nullable=True
    )

    content = Column(
        Text,
        nullable=False
    )

    event_date = Column(
        Date,
        nullable=False
    )

    source_url = Column(
        String(500),
        nullable=True
    )

    topic_id = Column(
        Integer,
        ForeignKey("topics.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    topic = relationship(
        "Topic",
        back_populates="articles"
    )

    tags = relationship(
        "Tag",
        secondary="article_tags",
        back_populates="articles"
    )