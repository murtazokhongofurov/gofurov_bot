import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from .constant import START_TEXT
from ..errors.error_handler import log_to_file
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(msg: types.Message):
    try:
        await db.add_user(chat_id=msg.from_user.id, first_name=msg.from_user.first_name)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.get_user(chat_id=msg.from_user.id)
    await msg.answer(text=START_TEXT.format(msg.from_user.first_name, msg.from_user.first_name))
