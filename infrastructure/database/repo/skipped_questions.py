from sqlalchemy.future import select
from infrastructure.database.models.skipped_question import SkippedQuestion
from infrastructure.database.repo.base import Database

class SkippedQuestionRepo:
    def __init__(self, db: Database):
        self.db = db

    # Methods for skipped questions
