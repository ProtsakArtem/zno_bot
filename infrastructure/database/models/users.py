from typing import Optional
from sqlalchemy import String, BIGINT, Boolean, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin, TableNameMixin

class User(Base, TimestampMixin, TableNameMixin):
    """
    This class represents a User in the application.

    Attributes:
        user_id (Mapped[int]): The unique identifier of the user.
        username (Mapped[Optional[str]]): The username of the user.
        full_name (Mapped[str]): The full name of the user.
        active (Mapped[bool]): Indicates whether the user is active or not.
        language (Mapped[str]): The language preference of the user.

    Methods:
        __repr__(): Returns a string representation of the User object.
    """
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[Optional[str]] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(128))
    active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    language: Mapped[str] = mapped_column(String(10), server_default=text("'en'"))
    current_topic: Mapped[Optional[int]] = mapped_column(ForeignKey('topics.topic_id'))
    current_question_index: Mapped[int] = mapped_column(BIGINT, default=0)
    progress_reset: Mapped[bool] = mapped_column(Boolean, default=False)

    answers = relationship("UserAnswer", back_populates="user")
    skipped_questions = relationship("SkippedQuestion", back_populates="user")

    def __repr__(self):
        return f"<User {self.user_id} {self.username} {self.full_name}>"
