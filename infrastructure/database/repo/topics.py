from sqlalchemy.future import select
from infrastructure.database.models.topic import Topic
from infrastructure.database.repo.base import Database

class TopicRepo:
    def __init__(self, db: Database):
        self.db = db

    async def get_all_topics(self):
        async with self.db.get_session() as session:
            result = await session.execute(select(Topic))
            return result.scalars().all()
