from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select
from infrastructure.database.models.question import Question
from infrastructure.database.repo.base import BaseRepo
import random

class QuestionRepo:
    def __init__(self, db: BaseRepo):
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


    async def add_question(self, topic_id,with_pictures,question_id, question_type, question_text, option_a, option_b, option_c, option_d, value_e, value_f, value_g, value_h, value_i, correct_option, question_number, picture, description, type2_answer):
        async with self.db.get_session() as session:
            await session.execute(
                insert(Question).values(question_id,topic_id, with_pictures, question_type, question_text, option_a, option_b, option_c, option_d, correct_option, question_number, value_e, value_f, value_g, value_h, value_i, picture, description, type2_answer)
            )
            await session.commit()
            print("Success")


    async def get_all_indexes(self):
        async with self.db.get_session() as session:
            result = await session.execute(
                select(Question.question_id)
            )
            question_ids = result.scalars().all()
        return question_ids

    async def get_answer_by_id(self, question_id):
        async with self.db.get_session() as session:
            result = await session.execute(
                select(Question.answer).where(Question.id == question_id)
            )
            answer = result.scalars.first()
            answer_result = answer.scalars().first()
            return answer_result

    async def get_question_data_by_count_theme(self, theme, count):
        async with self.db.get_session() as session:
            result = await session.execute(
                select(Question).where(Question.topic_id == theme and Question.question_number == count)
            )
            question = result.scalars().first()
            return question

    async def get_all_themes(self):
        async with self.db.get_session() as session:
            result = await session.execute(
                select(Question.topic_id)
            )
            themes = set(result.scalars().all())
            return themes


