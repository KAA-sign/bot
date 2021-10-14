from telegram import Bot
from telegram import Update

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from config import TG_TOKEN
# from config import TG_API_URL


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id = update.message.chat_id,
        text = "Привет! Коженый мешок",
    )


def do_first_bot(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = "Ваш ID = {}\n\n{}".format(chat_id, update.message.text)
    bot.send_message(
        chat_id = chat_id,
        text = text,
    )

def main():
    bot = Bot(
        token=TG_TOKEN,
        # base_url = TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_first_bot)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()