from aiogram import Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from infrastructure.database.repo.users import UserRepo
from infrastructure.database.repo.questions import QuestionRepo
from infrastructure.database.repo.topics import TopicRepo
from infrastructure.database.repo.user_answers import UserAnswerRepo
import random


class QuizStates(StatesGroup):
    answering = State()


def register_handlers(dp: Dispatcher, db):
    user_repo = UserRepo(db)
    question_repo = QuestionRepo(db)
    topic_repo = TopicRepo(db)
    user_answer_repo = UserAnswerRepo(db)

    router = Router()

    @router.message(commands=["start"])
    async def start_command(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        user = await user_repo.get_user_progress(user_id)

        if user:
            current_topic = user.current_topic
            current_question_index = user.current_question_index
        else:
            current_topic = 1  # assuming 1 is the default topic ID
            current_question_index = 0
            await user_repo.update_user_progress(user_id, current_topic, current_question_index)

        await send_question(message, question_repo, current_topic, current_question_index)
        await state.set_state(QuizStates.answering)

    @router.message(commands=["reset"])
    async def reset_progress_command(message: types.Message):
        user_id = message.from_user.id
        await user_repo.update_user_progress(user_id, None, 0)
        await message.answer("Your progress has been reset.")

    @router.message(commands=["random"])
    async def random_question_command(message: types.Message):
        user_id = message.from_user.id
        topics = await topic_repo.get_all_topics()
        random_topic = random.choice(topics)
        random_question = await question_repo.get_random_question(random_topic.topic_id)
        await send_question(message, question_repo, random_topic.topic_id, random_question.question_id)

    @router.callback_query(QuizStates.answering)
    async def answer_callback(callback_query: types.CallbackQuery, state: FSMContext):
        user_id = callback_query.from_user.id
        data = callback_query.data.split(':')
        question_id = int(data[0])
        selected_option = data[1]

        question = await question_repo.get_question(question_id)
        correct_option = question.correct_option

        is_correct = selected_option == correct_option
        await user_answer_repo.save_user_answer(user_id, question_id, selected_option, is_correct)

        response_text = "Correct!" if is_correct else f"Wrong. Correct answer: {correct_option}"
        await callback_query.message.answer(response_text)

        user = await user_repo.get_user_progress(user_id)
        current_topic = user.current_topic
        current_question_index = user.current_question_index + 1
        await user_repo.update_user_progress(user_id, current_topic, current_question_index)

        await send_question(callback_query.message, question_repo, current_topic, current_question_index)
        await state.set_state(QuizStates.answering)

    async def send_question(message: types.Message, question_repo, topic_id: int, question_index: int):
        question = await question_repo.get_question_by_index(topic_id, question_index)
        if not question:
            await message.answer("You have completed all questions in this topic!")
            return

        text = question.question_text
        buttons = [
            InlineKeyboardButton(text="A", callback_data=f"{question.question_id}:A"),
            InlineKeyboardButton(text="Б", callback_data=f"{question.question_id}:B"),
            InlineKeyboardButton(text="В", callback_data=f"{question.question_id}:C"),
            InlineKeyboardButton(text="Г", callback_data=f"{question.question_id}:D")
        ]

        if question.option_e:
            buttons.append(InlineKeyboardButton(text="Е", callback_data=f"{question.question_id}:E"))
        if question.option_f:
            buttons.append(InlineKeyboardButton(text="Ж", callback_data=f"{question.question_id}:F"))
        if question.option_g:
            buttons.append(InlineKeyboardButton(text="З", callback_data=f"{question.question_id}:G"))
        if question.option_h:
            buttons.append(InlineKeyboardButton(text="И", callback_data=f"{question.question_id}:H"))

        buttons.append(InlineKeyboardButton(text="Skip", callback_data=f"{question.question_id}:skip"))

        keyboard = InlineKeyboardMarkup(row_width=2).add(*buttons)
        await message.answer(text, reply_markup=keyboard)

    dp.include_router(router)
