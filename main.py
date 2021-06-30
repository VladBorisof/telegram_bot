import datetime
from logging import getLogger

from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler

from config import TG_TOKEN, TG_API_URL, debug_requests
from message_buttons import keyboard_callback_handler
from keyboard_buttons import BUTTON1_ADD, BUTTON2_HELP
from slash_functions import do_help, do_start

logger = getLogger(__name__)

TITLE, COUNT = range(2)

#
from telegram import ReplyKeyboardRemove


@debug_requests(logger)
def start_handler1(bot: Bot, update: Update):
    #  Спросить название траты
    update.message.reply_text(
        'Введите название траты, чтобы продолжить:',
    )
    return TITLE


@debug_requests(logger)
def title_handler(bot: Bot, update: Update, user_data: dict):
    # Получаем название траты
    user_data['title'] = update.message.text
    logger.info('user_data: %s', user_data)

    update.message.reply_text(
        'Введите сумму, которую Вы потратили:',
    )
    return COUNT


def validate_count(text):
    try:
        age = int(text)
    except (TypeError, ValueError):
        return None

    if age < 0:
        return None

    return age


@debug_requests(logger)
def count_handler(bot: Bot, update: Update, user_data: dict):
    # Получаем сумму траты
    count = validate_count(text=update.message.text)
    if count is None:
        update.message.reply_text('Пожалуйста введить сумму еще раз (не число):')
        return COUNT

    user_data['count'] = count
    logger.info('user_data: %s', user_data)

    # TODO: сохранить в базу
    # TODO: очистить user_data

    update.message.reply_text('Данные успешно сохранены.')
    return ConversationHandler.END


@debug_requests
def cancel_handler(bot: Bot, update: Update):
    """ Отменить весь процесс диалога. Данные будут утеряны"""
    update.message.reply_text('Отмена. Для начала с нуля нажмите /start')
    return ConversationHandler.END


@debug_requests(logger)
def do_echo(bot: Bot, update:Update):
    """Отправляет сообщение обратно"""
    text = update.message.text

    # keyboard button handler
    if text == BUTTON1_ADD:
        update.message.reply_text('/add')
        # return start_handler1(bot=bot, update=update)
    elif text == BUTTON2_HELP:
        return do_help(bot=bot, update=update)
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=text,
        )


def main():
    bot = Bot(token=TG_TOKEN, base_url=TG_API_URL)
    updater = Updater(bot=bot)

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('add', start_handler1),
        ],
        states={
            TITLE: [
                MessageHandler(Filters.all, title_handler, pass_user_data=True),
            ],
            COUNT: [
                MessageHandler(Filters.all, count_handler, pass_user_data=True),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    add_handler = CommandHandler("add", conv_handler)
    message_handler = MessageHandler(Filters.text, do_echo)
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)

    updater.dispatcher.add_handler(add_handler)
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(buttons_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()