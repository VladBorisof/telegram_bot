import datetime
from logging import getLogger

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ReplyKeyboardRemove

from config import debug_requests


logger = getLogger(__name__)

#
CALLBACK_BUTTON1_LEFT = "callback_button1_left"
CALLBACK_BUTTON2_RIGHT = "callback_button2_right"
CALLBACK_BUTTON3_MORE = "callback_button3_more"
CALLBACK_BUTTON4_BACK = "callback_button4_back"
CALLBACK_BUTTON5_HIDE_KEYBOARD = 'callback_button5_hide_keyboard'


# Названия кнопок
TITLES = {
    CALLBACK_BUTTON1_LEFT: "Показать историю сообщений",
    CALLBACK_BUTTON2_RIGHT: "Редактировать сообщение",
    CALLBACK_BUTTON3_MORE: "Дополнительно:",
    CALLBACK_BUTTON4_BACK: "Назад",
    CALLBACK_BUTTON5_HIDE_KEYBOARD: "Спрятать клавиатуру внизу"
}


@debug_requests(logger)
def get_base_inline_keyboard():
    """Делает клавиатуру. Видна под каждым сообщением."""
    # Каждый список внутри списка - один ряд кнопок.
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_LEFT], callback_data=CALLBACK_BUTTON1_LEFT),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_RIGHT], callback_data=CALLBACK_BUTTON2_RIGHT)
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_HIDE_KEYBOARD], callback_data=CALLBACK_BUTTON5_HIDE_KEYBOARD)
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_MORE], callback_data=CALLBACK_BUTTON3_MORE)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


@debug_requests(logger)
def get_keyboard2():
    """Делает дополнительное меню."""
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


@debug_requests(logger)
def keyboard_callback_handler(bot: Bot, update: Update, chat_data=None, **kwargs):
    """Обработчик всех кнопок со всех клавиатур."""
    query = update.callback_query
    data = query.data
    now = datetime.datetime.now()

    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    # Обработка кнопок
    if data == CALLBACK_BUTTON1_LEFT:
        # Убрать клавиатуру.
        query.edit_message_text(
            text = current_text,
            parse_mode=ParseMode.MARKDOWN,
        )
        bot.send_message(
            chat_id=chat_id,
            text='new message. \ncallback_query.data={}'.format(data),
            reply_markup=get_base_inline_keyboard()
        )
    elif data == CALLBACK_BUTTON2_RIGHT:
        # Редактируем клавиатуру. Текст оставляем.
        query.edit_message_text(
            text = "Успешно отредактировано",
            reply_markup=get_base_inline_keyboard()
        )
    elif data == CALLBACK_BUTTON3_MORE:
        # Показываем следующий экран клавиатуры.
        query.edit_message_text(
            text=current_text,
            reply_markup=get_keyboard2(),
        )
    elif data == CALLBACK_BUTTON4_BACK:
        query.edit_message_text(
            text=current_text,
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON5_HIDE_KEYBOARD:
        # Прячем клавиатуру под полем ввода.
            bot.send_message(
                chat_id=chat_id,
                text="Спрятали клавиатуру, чтобы ее вернуть введите: /start",
                reply_markup=ReplyKeyboardRemove(),
            )