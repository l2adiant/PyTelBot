import logging
import os

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = os.environ['API_kEY']
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.effective_chat.send_message("update.message_message")


def echo2(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.effective_chat.send_message(update.message.text)


def echo3(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.effective_chat.send_message("Couldnt recognize")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    buttons = ['old', 'asimold']
    buttons2 = ['new', 'asim']
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text(buttons) & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.text(buttons2) & ~Filters.command, echo2))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo3))

    # Start the Bot
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port=os.environ.get("PORT", 443), TOKEN, webhook_url="https://telegram-bot-asim.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
