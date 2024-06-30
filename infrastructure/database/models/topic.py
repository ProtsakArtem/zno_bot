from sqlalchemy import String, BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TableNameMixin

class Topic(Base, TableNameMixin):
    topic_id: Mapped[str] = mapped_column(VARCHAR(100), primary_key=True)
    topic_name: Mapped[str] = mapped_column(String(128), unique=True)

    questions = relationship("Question", back_populates="topic")
