import os
import logging
from io import BytesIO
from telegram import Update, ForceReply, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    if update.message:
        update.message.reply_text('Hi! I can decode and encode images. Send me an image and use the commands /decode or /encode to perform the respective action.')
    else:
        logger.warning('Received an update without a message.')


def decode_image(update: Update, _: CallbackContext) -> None:
    """Decode the image and send the decoded image."""
    # Get the photo file id
    photo_id = update.message.photo[-1].file_id
    # Download the photo file
    photo_file = BytesIO()
    update.message.bot.get_file(photo_id).download(out=photo_file)
    # Decode the image
    image = Image.open(photo_file)
    image = image.convert('RGB')
    data = image.tobytes()
    # Send the decoded image
    update.message.reply_photo(photo=data)

def encode_image(update: Update, _: CallbackContext) -> None:
    """Encode the decoded image and send the encoded image."""
    # Get the photo file id
    photo_id = update.message.photo[-1].file_id
    # Download the photo file
    photo_file = BytesIO()
    update.message.bot.get_file(photo_id).download(out=photo_file)
    # Decode the image
    image = Image.open(photo_file)
    image = image.convert('RGB')
    data = image.tobytes()
    # Encode the image
    image = Image.frombytes('RGB', image.size, data)
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    # Send the encoded image
    update.message.reply_photo(photo=buffer.getvalue())

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it the bot's token
    updater = Updater("5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers for commands and messages
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("decode", decode_image))
    dispatcher.add_handler(CommandHandler("en", encode_image))

    # Start the bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
