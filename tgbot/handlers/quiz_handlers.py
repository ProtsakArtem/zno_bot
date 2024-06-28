from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from infrastructure.database.repo.database import Database
import random

from tgbot.handlers.user import send_question


class QuizStates(StatesGroup):
    answering = State()


def register_handlers(dp: Dispatcher, db: Database):
    dp.message.register(start_command, F.command == "start")
    dp.message.register(reset_progress_command, F.command == "reset")
    dp.message.register(random_question_command, F.command == "random")
    dp.callback_query.register(answer_callback, QuizStates.answering)


async def start_command(message: types.Message, state: FSMContext, db: Database):
    user_id = message.from_user.id
    user = await db.get_user_progress(user_id)

    if user:
        current_topic = user.current_topic
        current_question_index = user.current_question_index
    else:
        current_topic = 1  # припустимо, що 1 - ідентифікатор теми за замовчуванням
        current_question_index = 0
        await db.update_user_progress(user_id, current_topic, current_question_index)

    await send_question(message, db, current_topic, current_question_index)
    await state.set_state(QuizStates.answering)


async def reset_progress_command(message: types.Message, db: Database):
    user_id = message.from_user.id
    await db.update_user_progress(user_id, None, 0)
    await message.answer("Ваш прогрес було скинуто.")


async def random_question_command(message: types.Message, db: Database):
    user_id = message.from_user.id
    topics = await db.get_all_topics()
    random_topic = random.choice(topics)
    random_question = await db.get_random_question(random_topic.topic_id)
    await send_question(message, db, random_topic.topic_id, random_question.question_id)


async def answer_callback(callback_query: types.CallbackQuery, state: FSMContext, db: Database):
    user_id = callback_query.from_user.id
    data = callback_query.data.split(':')
    question_id = int(data[0])
    selected_option = data[1]


