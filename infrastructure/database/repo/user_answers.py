from sqlalchemy.future import select
from infrastructure.database.models.user_answer import UserAnswer
from infrastructure.database.repo.base import Database

class UserAnswerRepo:
    def __init__(self, db: Database):
        self.db = db

    async def save_user_answer(self, user_id, question_id, selected_option, is_correct):
        async with self.db.get_session() as session:
            user_answer = UserAnswer(
                user_id=user_id,
                question_id=question_id,
                selected_option=selected_option,
                is_correct=is_correct
            )
            session.add(user_answer)
            await session.commit()
