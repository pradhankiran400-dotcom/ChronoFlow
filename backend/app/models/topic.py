from datetime import datetime
from app.database.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, DateTime,Text
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base

class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True,nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    articles = relationship("Article", back_populates="topic",cascade="all, delete")