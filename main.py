import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image
import random
import io
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Change the following key to your own secret key
KEY = b'mysecretpassword'

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

    # Convert the image to a byte stream
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    # Pad the image bytes to be a multiple of the AES block size
    padded_img_bytes = pad(img_bytes.read(), AES.block_size)

    # Generate a random initialization vector (IV)
    iv = bytes([random.randint(0, 255) for i in range(AES.block_size)])

    # Encrypt the padded image bytes using AES in CBC mode with the IV and key
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted_img_bytes = iv + cipher.encrypt(padded_img_bytes)

    # Send the encrypted image
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=io.BytesIO(encrypted_img_bytes))

def decrypt_image(update, context):
    # Check if the message is a reply and contains an image
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please reply to an image message with /dy to decrypt.")
        return

    # Get the file ID of the largest version of the photo in the replied message
    file_id = update.message.reply_to_message.photo[-1].file_id

    # Download the image
    file = context.bot.get_file(file_id)
    encrypted_img_bytes = io.BytesIO(file.download_as_bytearray()).read

    # Get the initialization vector (IV) and encrypted image data from the byte stream
    iv = encrypted_img_bytes[:AES.block_size]
    encrypted_img_data = encrypted_img_bytes[AES.block_size:]

    # Decrypt the image using AES in CBC mode
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    padded_img_data = cipher.decrypt(encrypted_img_data)

    # Unpad the decrypted image
    unpadder = unpad(bytes(padded_img_data), AES.block_size)
    img_data = unpadder.update(padded_img_data) + unpadder.finalize()

    # Create a new image with the same dimensions and the decrypted pixel values
    img = Image.open(io.BytesIO(img_data))
    width, height = img.size

    # Save the decrypted image to a buffer
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)

    # Send the decrypted image
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=buffer)
 

def main():
    # Create the Updater and pass it the bot's token
    updater = Updater(TOKEN, use_context=True)

    # Add handlers for the /start, /en, and /dy commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('en', encrypt_image))
    updater.dispatcher.add_handler(CommandHandler('dy', decrypt_image))

    # Start the bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

