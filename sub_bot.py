try:
    from PIL import Image
except ImportError:
    import Image

import numpy as np


from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from telegram import Update, Bot, ParseMode 
import os


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    # bot.send_photo(photo=open('1.png', 'rb'))
    update.message.reply_text('Hi! \n\nWelcome to subtitle creation bot . \n\nJust send a video file to the bot and it will send the subtitle file back \n')

def search(bot, update):
    """Send reply of user's message."""
    photo_file = bot.get_file(update.message.video.file_id)
    print("got the file ")
    photo_file.download('data/input.mp4')
    print("downloaded")

    command4="python3 autosub/main.py --file data/input.mp4"
    os.system(command4)

    command7="rm audio/*"
    os.system(command7)





    update.message.reply_document(document=open('output/input.srt', 'rb'))

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    bot_token=os.environ.get("BOT_TOKEN", "")
    updater = Updater(bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video, search))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
