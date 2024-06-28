from sqlalchemy import BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TableNameMixin

class SkippedQuestion(Base, TableNameMixin):
    skipped_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.question_id'))

    user = relationship("User", back_populates="skipped_questions")
    question = relationship("Question", back_populates="skipped_questions")
