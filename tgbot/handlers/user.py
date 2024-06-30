from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from infrastructure.database.repo import database as Database
import random

class QuizStates(StatesGroup):
    answering = State()

bot = Bot(token='YOUR_BOT_TOKEN')
dp = Dispatcher(storage=MemoryStorage())
router = Router()

@router.message(F.command == "start")
async def start_command(message: Message, state: FSMContext, db: Database):
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

@router.message(F.command == "reset")
async def reset_progress_command(message: Message, db: Database):
    user_id = message.from_user.id
    await db.update_user_progress(user_id, None, 0)
    await message.answer("Ваш прогрес було скинуто.")


@router.message(F.command == "random")
async def random_question_command(message: Message, db: Database):
    user_id = message.from_user.id
    topics = await db.get_all_topics()
    random_topic = random.choice(topics)
    random_question = await db.get_random_question(random_topic.topic_id)
    await send_question(message, db, random_topic.topic_id, random_question.question_id)


@router.message(F.command == "get_themes")
async def random_question_command(message: Message, db: Database, bot: Bot):
    user_id = message.from_user.id
    topics = await db.get_all_topics()
    await bot.send_message(message.from_user.id, topics)

@router.callback_query(QuizStates.answering)
async def answer_callback(callback_query: CallbackQuery, state: FSMContext, db: Database):
    user_id = callback_query.from_user.id
    data = callback_query.data.split(':')
    question_id = int(data[0])
    selected_option = data[1]

    question = await db.get_question(question_id)
    correct_option = question.correct_option

    is_correct = selected_option == correct_option
    await db.save_user_answer(user_id, question_id, selected_option, is_correct)

    if is_correct:
        response_text = "Правильно!"
    else:
        response_text = f"Неправильно. Правильна відповідь: {correct_option}"

    await callback_query.message.answer(response_text)

    user = await db.get_user_progress(user_id)
    current_topic = user.current_topic
    current_question_index = user.current_question_index + 1
    await db.update_user_progress(user_id, current_topic, current_question_index)

    await send_question(callback_query.message, db, current_topic, current_question_index)
    await state.set_state(QuizStates.answering)




async def send_question(message: Message, db: Database, topic_id: int, question_index: int):
    question = await db.get_question_by_index(topic_id, question_index)
    if not question:
        await message.answer("Ви завершили всі питання з цієї теми!")
        return

    text = question.question_text
    buttons = [
        [InlineKeyboardButton(text="A", callback_data=f"{question.question_id}:A")],
        [InlineKeyboardButton(text="Б", callback_data=f"{question.question_id}:B")],
        [InlineKeyboardButton(text="В", callback_data=f"{question.question_id}:C")],
        [InlineKeyboardButton(text="Г", callback_data=f"{question.question_id}:D")],
        [InlineKeyboardButton(text="Пропустити", callback_data=f"{question.question_id}:skip")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    await message.answer(text, reply_markup=keyboard)

dp.include_router(router)

if __name__ == "__main__":
    dp.run_polling(bot)
