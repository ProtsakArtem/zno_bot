from sqlalchemy import String, BIGINT, ForeignKey, Boolean, Integer, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TableNameMixin

class Question(Base, TableNameMixin):
    question_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    question_number: Mapped[int] = mapped_column(Integer)
    topic_id: Mapped[str] = mapped_column(VARCHAR(100), ForeignKey('topics.topic_id'))
    with_pictures: Mapped[bool] = mapped_column(Boolean)
    #1 - deafult question, 2-відпов
    question_type: Mapped[int] = mapped_column(Integer, default=1)
    question_text: Mapped[str] = mapped_column(String)
    option_a: Mapped[str] = mapped_column(String)
    option_b: Mapped[str] = mapped_column(String)
    option_c: Mapped[str] = mapped_column(String)
    option_d: Mapped[str] = mapped_column(String)
    value_e: Mapped[str] = mapped_column(String, nullable=True, default=None)
    value_f: Mapped[str] = mapped_column(String, nullable=True, default=None)
    value_g: Mapped[str] = mapped_column(String, nullable=True, default=None)
    value_h: Mapped[str] = mapped_column(String, nullable=True, default=None)
    value_i: Mapped[str] = mapped_column(String, nullable=True, default=None)
    correct_option: Mapped[str] = mapped_column(String)
    picture: Mapped[str] = mapped_column(String, nullable=True, default=None)
    description: Mapped[str] = mapped_column(String)
    type2_answer: Mapped[str] = mapped_column(String, nullable=True, default=None)


    topic = relationship("Topic", back_populates="questions")
    answers = relationship("UserAnswer", back_populates="question")
    skipped_questions = relationship("SkippedQuestion", back_populates="question")
