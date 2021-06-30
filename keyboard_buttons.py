from telegram import KeyboardButton, ReplyKeyboardMarkup

BUTTON1_ADD = "Добавить запись"
BUTTON2_HELP = "Помощь"


def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON1_ADD),
            KeyboardButton(BUTTON2_HELP),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )