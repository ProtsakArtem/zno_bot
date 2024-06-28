from sqlalchemy import String, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TableNameMixin

class Topic(Base, TableNameMixin):
    topic_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    topic_name: Mapped[str] = mapped_column(String(128), unique=True)

    questions = relationship("Question", back_populates="topic")
