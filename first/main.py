from asyncio import current_task
import datetime
from sre_constants import CALL
from subprocess import Popen
from subprocess import PIPE

from telegram import Bot
from telegram import Update
from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler


from config import load_config


# 'callback_data' - это то, что будет присылать бот при нажатии на каждую ктопку.

CALLBACK_BUTTON1_LEFT = 'callback_button1_left'
CALLBACK_BUTTON2_RIGTH = 'callback_button2_right'
CALLBACK_BUTTON3_MORE = 'callback_button3_more'
CALLBACK_BUTTON4_BACK = 'callback_button4_back'
CALLBACK_BUTTON5_TIME = 'callback_button5_time'
CALLBACK_BUTTON6_PRICE = 'callback_button6_price'
CALLBACK_BUTTON7_PRICE = 'callback_button7_price'
CALLBACK_BUTTON8_PRICE = 'callback_button8_price'

TITLES = {
    CALLBACK_BUTTON1_LEFT: 'Новое сообщение &#9993',
    CALLBACK_BUTTON2_RIGTH: 'Отредактировать &#9998',
    CALLBACK_BUTTON3_MORE: 'Ещё &#8230',
    CALLBACK_BUTTON4_BACK: 'Назад &#8678',
    CALLBACK_BUTTON5_TIME: 'Время &#9200',
    CALLBACK_BUTTON6_PRICE: 'USD $',
    CALLBACK_BUTTON7_PRICE: 'EUR &#8364',
    CALLBACK_BUTTON8_PRICE: 'Brent &#128738',
}

def get_base_inline_keyboard():
    '''Базовая клавиатура'''
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_LEFT], callback_data=CALLBACK_BUTTON1_LEFT),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_RIGTH], callback_data=CALLBACK_BUTTON2_RIGTH),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_MORE], callback_data=CALLBACK_BUTTON3_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_keyboard2():
    '''Вложенная клавиатура'''
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_TIME], callback_data=CALLBACK_BUTTON5_TIME),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_PRICE], callback_data=CALLBACK_BUTTON6_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_PRICE], callback_data=CALLBACK_BUTTON7_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON8_PRICE], callback_data=CALLBACK_BUTTON8_PRICE),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def keyboard_callback_hendler(bot: Bot, update: Update, chat_data=None, **kwargs):
    '''Обработчик всех кнопок со всех клавиатур'''
    query = update.callback_query
    data = query.data
    now = datetime.datetime.now()

    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    if data == CALLBACK_BUTTON1_LEFT:
        # Убираем клавиатуру
        query.edit_message_text(text=current_text, parse_mode=ParseMode.MARKDOWN,)

        # Отправляем новое сообщение при нажатии на кнопку
        bot.send_message(
            chat_id=chat_id,
            text="Новое сообщение\n\ncollback_query.data={}".format(data),
            reply_markup=get_base_inline_keyboard(),
            )
    elif data == CALLBACK_BUTTON2_RIGTH:
        # Редактируем сообщение, но оставляем клавиатуру
        query.edit_message_text(
            text="Успешно отредактировано в {}".format(now),
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON3_MORE:
        # Вложенная клавиатура
        # Остаётся тот же текст
        query.edit_message_text(
            text=current_text,
            reply_markup=get_keyboard2(),
        )
    elif data == CALLBACK_BUTTON4_BACK:
        # Предидущий экран клавиатуры
        # Остаётся тот же текст
         query.edit_message_text(
            text=current_text,
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON5_TIME:
        # Новый текст, старая клавиатура
        text = "*Точное время*\n\n{}".format(now)
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_keyboard2(),
        )
    elif data in (CALLBACK_BUTTON6_PRICE, CALLBACK_BUTTON7_PRICE):
        pair = {
            CALLBACK_BUTTON6_PRICE: "USD",
            CALLBACK_BUTTON7_PRICE: "EUR",
        }[data]
        try:
            current_price = client.get_last_price(pair=pair)
            text = "*Курс валюты*\n\n*{}* = {}$".format(pair, current_price)
        except CbrError:
            text = "Произошла ошибка :(\n\nПопробуйте ещё раз"
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_keyboard2(),
        )

def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id = update.message.chat_id,
        text = "Привет! Коженый мешок!",
        reply_markup=get_base_inline_keyboard(),
    )

def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id = update.message.chat_id,
        text="Это учебный бот\n\n"
            "Список доступных команд есть в меню\n\n"
            "Так же я отвечаю на любое сообщение",
        reply_markup=get_base_inline_keyboard(),
    )

def do_time(bot: Bot, update: Update):
    """Узнать серверное время
    """
    process = Popen("date", stdout=PIPE)
    text, error = process.communicate()
    if error:
        text = "Произошла ошибка, время неизвестно"
    else:
        # Декодировать
        text = text.decode("utf-8")
        
    bot.send_message(
        chat_id = update.message.chat_id,
        text = text,
        reply_markup=get_base_inline_keyboard(),
    )

def do_first_bot(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = "Ваш ID = {}\n\n{}".format(chat_id, update.message.text)
    bot.send_message(
        chat_id = chat_id,
        text = text,
        reply_markup=get_base_inline_keyboard(),
    )

def main():
    config = load_config()
    bot = Bot(
        token=config.TG_TOKEN,
        # base_url = config.TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    time_handler = CommandHandler("time", do_time)
    message_handler = MessageHandler(Filters.text, do_first_bot)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()