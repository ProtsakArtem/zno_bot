from sqlalchemy.future import select
from infrastructure.database.models.question import Question
from infrastructure.database.repo.base import Database
import random

class QuestionRepo:
    def __init__(self, db: Database):
        self.db = db

    async def get_random_question(self, topic_id):
        async with self.db.get_session() as session:
            result = await session.execute(select(Question).where(Question.topic_id == topic_id))
            questions = result.scalars().all()
            return random.choice(questions)

    async def get_question(self, question_id):
        async with self.db.get_session() as session:
            result = await session.execute(select(Question).where(Question.question_id == question_id))
            return result.scalars().first()

    async def get_question_by_index(self, topic_id, question_index):
        async with self.db.get_session() as session:
            result = await session.execute(
                select(Question)
                .where(Question.topic_id == topic_id)
                .order_by(Question.question_id)
                .offset(question_index)
                .limit(1)
            )
            return result.scalars().first()
