from logging import getLogger

from telegram import Bot, Update

from keyboard_buttons import get_base_reply_keyboard
from config import debug_requests

logger = getLogger(__name__)


@debug_requests(logger)
def do_start(bot: Bot, update: Update):
    """Обработчик /start"""
    bot.send_message(
        chat_id=update.message.chat_id,
        text="hi, send me anything!",
        reply_markup=get_base_reply_keyboard()
    )


@debug_requests(logger)
def do_help(bot: Bot, update: Update):
    """Обработчик /help"""
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Справка."
    )