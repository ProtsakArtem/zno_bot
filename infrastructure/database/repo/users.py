import asyncio
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.database.models import Question, Base
from infrastructure.database.repo.questions import QuestionRepo

DATABASE_URL = "postgresql+asyncpg://mainsempai:oraoraora123@localhost:1488/database"  # Замініть на ваші дані

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def fetch_records_from_sqlite():
    # Підключення до бази даних SQLite
    conn = sqlite3.connect('zno_questions.db')
    cursor = conn.cursor()

    # Витягуємо дані з таблиці
    cursor.execute('SELECT * FROM history')

    # Підключення до PostgreSQL
    async with SessionLocal() as session:
        async with session.begin():
            for row in cursor.fetchall():
                if row[0] == '' or row[0] == None:
                    continue
                topic = row[0]
                q_count = row[2]
                q_text = row[3]
                picture = row[-1]
                with_picture = picture is not None and picture != 0
                description = row[-2]

                a = row[-2].strip().replace(".", "").split("\n")[-1].lower()
                if "відповідь" in a:
                    b = a.index("відповідь")
                else:
                    b = a.index("відповіді")
                ans = a[b + 11:].strip()
                ans_2 = None
                var_a, var_b, var_c, var_d = row[4], row[5], row[6], row[7]
                var_e, var_f, var_g, var_h, var_i = None, None, None, None, None
                q_type = 1 if row[8] == 0 else 2

                if q_type == 2:
                    b4 = ans.replace(",", "").replace("–", "").replace("-", "").replace(" ", "").replace("1",
                                                                                                         "").replace(
                        "2", "").replace("3", "").replace("4", "").replace(" ", "")
                    las = " ".join([f"{x + 1}-{b4[x]}" for x in range(len(b4))])
                    ans_2 = las.rstrip()
                    ans = None
                    var_e, var_f, var_g, var_h, var_i = row[8], row[9], row[10], row[11], row[12]

                question = Question(
                    question_number=q_count,
                    topic_id=topic,
                    with_pictures=with_picture,
                    question_type=q_type,
                    question_text=q_text,
                    option_a=var_a,
                    option_b=var_b,
                    option_c=var_c,
                    option_d=var_d,
                    correct_option=ans,
                    value_e=var_e,
                    value_f=var_f,
                    value_g=var_g,
                    value_h=var_h,
                    value_i=var_i,
                    picture=picture,
                    description=description,
                    type2_answer=ans_2
                )
                session.add(question)

            await session.commit()

    conn.close()


# Виклик функції для виведення записів
asyncio.run(fetch_records_from_sqlite())
