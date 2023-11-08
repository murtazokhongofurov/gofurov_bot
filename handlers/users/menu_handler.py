from aiogram import types
from ..errors.error_handler import log_to_file
from loader import dp, db
from .constant import RECEIVE_TEXT_MESSAGE, USER_MESSAGE
from data.config import ADMINS


@dp.message_handler(content_types=types.ContentType.TEXT)
async def menu_handler(msg: types.Message):
    await msg.answer(text=RECEIVE_TEXT_MESSAGE)
    try:
        await db.update_user_message(chat_id=msg.from_user.id, message=msg.text)
        for admin in ADMINS:
            await dp.bot.send_message(chat_id=admin, text=USER_MESSAGE.format(msg.from_user.first_name, msg.text))
    except Exception as e:
        log_to_file("errors", f"Error update message and send admin message: {e}")
