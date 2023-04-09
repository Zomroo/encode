import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image
import random
import io

TOKEN = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot that can encrypt images. To encrypt an image, send me an image and use the /en command.")

def encrypt_image(update, context):
    # Check if the message is a reply and contains an image
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please reply to an image message with /en to encrypt.")
        return

    # Get the file ID of the largest version of the photo in the replied message
    file_id = update.message.reply_to_message.photo[-1].file_id

    # Download the image
    file = context.bot.get_file(file_id)
    img_bytes = io.BytesIO(file.download_as_bytearray())

    # Open the image from the byte stream
    img = Image.open(img_bytes)

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

def decrypt_image(update, context):
    # Check if the message is a reply and contains an image
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please reply to an image message with /dy to decrypt.")
        return

    # Get the file ID of the largest version of the photo in the replied message
    file_id = update.message.reply_to_message.photo[-1].file_id

    # Download the image
    file = context.bot.get_file(file_id)
    img_bytes = io.BytesIO(file.download_as_bytearray())

    # Open the image from the byte stream
    img = Image.open(img_bytes)

    # Get the dimensions of the image
    width, height = img.size

    # Get the pixel values of the encrypted image
    pixels = list(img.getdata())

    # Make a copy of the pixel values and shuffle the copy to get the original pixel values
    original_pixels = pixels.copy()
    random.shuffle(original_pixels)

    # Create a new image with the same dimensions and the decrypted pixel values
    decrypted_img = Image.new('RGB', (width, height))
    decrypted_img.putdata(original_pixels)

    # Save the decrypted image to a buffer
    buffer = io.BytesIO()
    decrypted_img.save(buffer, format='JPEG')
    buffer.seek(0)

    # Send the decrypted image
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=buffer)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Add handlers for the /start, /en, and /dy commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('en', encrypt_image))
    updater.dispatcher.add_handler(CommandHandler('dy', decrypt_image))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
