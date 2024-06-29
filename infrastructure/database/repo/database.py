from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from infrastructure.database.models import Base
from tgbot.config import load_config
from infrastructure.database.models.users import User
from infrastructure.database.models.topic import Topic
from infrastructure.database.models.question import Question
from infrastructure.database.models.user_answer import UserAnswer
from infrastructure.database.models.skipped_question import SkippedQuestion
import random

config = load_config()
DATABASE_URL = config.db.construct_sqlalchemy_url()

class Database:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL, echo=True)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def connect(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def disconnect(self):
        await self.engine.dispose()

    async def get_user_progress(self, user_id):
        async with self.async_session() as session:
            result = await session.execute(select(User).where(User.user_id == user_id))
            return result.scalars().first()

    async def update_user_progress(self, user_id, current_topic, current_question_index):
        async with self.async_session() as session:
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().first()
            if user:
                user.current_topic = current_topic
                user.current_question_index = current_question_index
            await session.commit()

    async def get_all_topics(self):
        async with self.async_session() as session:
            result = await session.execute(select(Topic))
            return result.scalars().all()

    async def get_random_question(self, topic_id):
        async with self.async_session() as session:
            result = await session.execute(select(Question).where(Question.topic_id == topic_id))
            questions = result.scalars().all()
            return random.choice(questions)

    async def get_question(self, question_id):
        async with self.async_session() as session:
            result = await session.execute(select(Question).where(Question.question_id == question_id))
            return result.scalars().first()

    async def save_user_answer(self, user_id, question_id, selected_option, is_correct):
        async with self.async_session() as session:
            user_answer = UserAnswer(
                user_id=user_id,
                question_id=question_id,
                selected_option=selected_option,
                is_correct=is_correct
            )
            session.add(user_answer)
            await session.commit()

    async def get_question_by_index(self, topic_id, question_index):
        async with self.async_session() as session:
            result = await session.execute(
                select(Question)
                .where(Question.topic_id == topic_id)
                .order_by(Question.question_id)
                .offset(question_index)
                .limit(1)
            )
            return result.scalars().first()
