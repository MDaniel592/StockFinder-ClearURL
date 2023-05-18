#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import re

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from unalix._core import clear_url

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_CHANNEL = os.environ.get("TELEGRAM_CHANNEL", None)
AMAZON_REFER = "?&linkCode=ll1&tag=stockfinder09-21"
CHARS_TO_SCAPE = r"_*\[\]()~`>#\+\-=\|{}\.!"
USER_THANKS_MSG = "Gracias por hacer uso de \\@SF\\_Validator \\. Su nuevo enlace\\: \n"

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    chat_id = update.effective_message.chat_id

    logger.warning(f"chat_id: {chat_id}- {user.username} - {user.first_name}  - Replied his ID")
    update.message.reply_markdown_v2(rf"Hola {user.mention_markdown_v2()}\! Su ID de telegram es {chat_id}")


def help_command(update: Update, context: CallbackContext) -> None:
    msg = "Soy un bot que se encarga de limpiar los referidos. Si dispongo de algún referido propio lo añado! " + "Envíame un mensaje con un enlace y probamos"
    update.message.reply_text(msg)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    user = update.effective_user

    chat_id = update.effective_message.chat_id
    orig_msg = update.effective_message.text_html

    logger.warning(f"chat_id: {chat_id} - username: {user.username} - {user.first_name} - msg: {orig_msg}")
    message_id = update.effective_message.message_id

    orig_url = re.findall(r'https?:\/\/[^\s<>"]+|www\.[^\s<>"]+', orig_msg)
    logger.warning(f"chat_id: {chat_id} - username: {user.username} - {user.first_name} - orig_url: {orig_url}")
    if not orig_url:
        return
    orig_url = orig_url[0]
    if AMAZON_REFER in orig_url:
        return

    new_url = clear_url(orig_url)
    logger.warning(f"chat_id: {chat_id} - username: {user.username} - {user.first_name} - new_url: {new_url}")

    if "amazon" in new_url:
        new_url = new_url + AMAZON_REFER

    if new_url == orig_url:
        return

    logger.warning(f"chat_id: {chat_id} - username: {user.username} - {user.first_name} - new_url: {new_url}")
    new_msg = re.sub(r'https?:\/\/[^\s<>"]+|www\.[^\s<>"]+', new_url, orig_msg, flags=re.MULTILINE)
    logger.warning(f"chat_id: {chat_id} - username: {user.username} - {user.first_name} - new_msg: {new_msg}")

    if new_msg == orig_msg:
        return

    new_msg = re.sub(f"([{re.escape(CHARS_TO_SCAPE)}])", r"\\\\1", new_msg)

    if chat_id == int(TELEGRAM_CHANNEL):
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        msg = f"Mensaje de {user.first_name} editado\\. Nuevo mensaje\\: \n" + new_msg
        context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="MarkdownV2")
    else:
        msg = USER_THANKS_MSG + new_msg
        context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="MarkdownV2")

    logger.warning(f"chat_id: {chat_id} - username: {user.username} - {user.first_name} - msg: {msg}")


def main() -> None:
    token = os.environ.get("TELEGRAM_TOKEN", None)
    if not token:
        logger.warning(f"No existe el token")
        return

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    logger.warning(f"Se inicia el BOT")
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
