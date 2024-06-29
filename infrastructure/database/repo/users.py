from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Mapped

from infrastructure.database.models import User
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
        full_name: str,
        language: str,
        username: Optional[str] = None,

    ):
        """
        Creates or updates a new user in the database and returns the user object.
        :param user_id: The user's ID.
        :param full_name: The user's full name.
        :param language: The user's language.
        :param username: The user's username. It's an optional parameter.
        :return: User object, None if there was an error while making a transaction.
        """

        insert_stmt = (
            insert(User)
            .values(
                user_id=user_id,
                username=username,
                full_name=full_name,
                language=language,
            )
            .on_conflict_do_update(
                index_elements=[User.user_id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                ),
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def get_user_progress(self, user_id):
        async with self.db.get_session() as session:
            result = await session.execute(select(User).where(User.user_id == user_id))
            return result.scalars().first()

    async def update_user_progress(self, user_id, current_topic, current_question_index):
        async with self.db.get_session() as session:
            result = await session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().first()
            if user:
                user.current_topic = current_topic
                user.current_question_index = current_question_index
            await session.commit()