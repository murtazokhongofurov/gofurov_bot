import logging
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted)

from loader import dp
import os
import datetime

LOG_FOLDER = "./logs"


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(exception, CantDemoteChatCreator):
        logging.exception("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logging.exception('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logging.exception('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.exception('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.exception('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.exception(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    logging.exception(f'Update: {update} \n{exception}')


def log_to_file(folder, *msg):
    now = datetime.datetime.now()
    timestamp = now.strftime("[%Y-%m-%d %H:%M:%S,%f]")

    yy = now.strftime("%Y")
    mm = now.strftime("%m")
    dd = now.strftime("%d")

    file_path = os.path.join(LOG_FOLDER, folder, yy, mm, dd)

    os.makedirs(file_path, exist_ok=True)

    file_name = os.path.join(file_path, "bot.log")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(file_name, mode="a", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    msg_with_timestamp = timestamp + " " + " ".join(map(str, msg))
    logger = logging.getLogger()
    logger.info(" ".join(map(str, msg)))
    with open(file_name, "a") as f:
        f.write(msg_with_timestamp + "\n")
