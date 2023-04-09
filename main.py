import logging
import os
import tempfile
import imghdr

from io import BytesIO
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PIL import Image

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me an image and I will encrypt it.')

def encrypt_image(update: Update, context: CallbackContext) -> None:
    try:
        # Get the image file
        file = update.message.photo[-1].get_file()

        # Check if the file is an image
        if imghdr.what(file) is None:
            update.message.reply_text('Invalid image file.')
            return

        # Read the image file into memory
        img_data = file.download_as_bytearray()

        # Encrypt the image data
        key = os.urandom(1)[0]  # Generate a random key
        encrypted_data = bytearray([b ^ key for b in img_data])

        # Send the encrypted image back to the user
        file = BytesIO(encrypted_data)
        file.name = 'encrypted.jpg'
        update.message.reply_photo(photo=file, caption=f'Encryption key: {key}')

    except Exception as e:
        logger.error(str(e))
        update.message.reply_text('An error occurred while encrypting the image.')

def decrypt_image(update: Update, context: CallbackContext) -> None:
    try:
        # Get the image file
        file = update.message.photo[-1].get_file()

        # Check if the file is an image
        if imghdr.what(file) is None:
            update.message.reply_text('Invalid image file.')
            return

        # Read the image file into memory
        img_data = file.download_as_bytearray()

        # Get the encryption key
        key = int(update.message.reply_to_message.caption.split(':')[-1])

        # Decrypt the image data
        decrypted_data = bytearray([b ^ key for b in img_data])

        # Send the decrypted image back to the user
        with tempfile.NamedTemporaryFile(suffix='.jpg') as temp:
            temp.write(decrypted_data)
            temp.flush()
            update.message.reply_photo(photo=open(temp.name, 'rb'))

    except Exception as e:
        logger.error(str(e))
        update.message.reply_text('An error occurred while decrypting the image.')

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater('5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk')

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo & Filters.reply & Filters.regex('^en$'), encrypt_image))
    dispatcher.add_handler(MessageHandler(Filters.photo & Filters.reply & Filters.regex('^dy$'), decrypt_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
