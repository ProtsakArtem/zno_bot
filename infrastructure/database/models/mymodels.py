from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    current_topic = Column(Integer, ForeignKey('topics.topic_id'))
    current_question_index = Column(Integer)
    progress_reset = Column(Boolean, default=False)

    answers = relationship("UserAnswer", back_populates="user")
    skipped_questions = relationship("SkippedQuestion", back_populates="user")

class Topic(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key=True)
    topic_name = Column(String, unique=True)

    questions = relationship("Question", back_populates="topic")

class Question(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))
    question_text = Column(String)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    correct_option = Column(String)

    topic = relationship("Topic", back_populates="questions")
    answers = relationship("UserAnswer", back_populates="question")
    skipped_questions = relationship("SkippedQuestion", back_populates="question")

class UserAnswer(Base):
    __tablename__ = 'user_answers'
    answer_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    question_id = Column(Integer, ForeignKey('questions.question_id'))
    selected_option = Column(String)
    is_correct = Column(Boolean)

    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")

class SkippedQuestion(Base):
    __tablename__ = 'skipped_questions'
    skipped_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    question_id = Column(Integer, ForeignKey('questions.question_id'))

    user = relationship("User", back_populates="skipped_questions")
    question = relationship("Question", back_populates="skipped_questions")
