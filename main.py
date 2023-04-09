import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image
import random

TOKEN = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot that can encrypt images. To encrypt an image, send me an image and use the /en command.")

def encrypt_image(update, context):
    # Check if the message contains an image
    if not update.message.photo:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please send an image to encrypt.")
        return

    # Get the file ID of the largest version of the photo
    file_id = update.message.photo[-1].file_id

    # Download the image
    file = context.bot.get_file(file_id)
    img = Image.open(file.download_as_bytearray())

    # Get the dimensions of the image
    width, height = img.size

    # Encrypt the image by shuffling the pixel values
    pixels = list(img.getdata())
    random.shuffle(pixels)

    # Create a new image with the same dimensions and the encrypted pixel values
    encrypted_img = Image.new('RGB', (width, height))
    encrypted_img.putdata(pixels)

    # Save the encrypted image to a buffer
    buffer = io.BytesIO()
    encrypted_img.save(buffer, format='JPEG')
    buffer.seek(0)

    # Send the encrypted image
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=buffer)

def main():
    updater = Updater(TOKEN, use_context=True)

    # Add handlers for the /start and /en commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('en', encrypt_image))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
