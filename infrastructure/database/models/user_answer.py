from sqlalchemy import String, BIGINT, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TableNameMixin

class UserAnswer(Base, TableNameMixin):
    answer_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.question_id'))
    selected_option: Mapped[str] = mapped_column(String)
    is_correct: Mapped[bool] = mapped_column(Boolean)

    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")
