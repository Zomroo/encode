import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from io import BytesIO
from PIL import Image


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Image Encryption Bot!")


def encrypt_image(update, context):
    # Check if the reply message is an image
    if update.message.reply_to_message.photo:
        # Get the image file_id
        file_id = update.message.reply_to_message.photo[-1].file_id
        # Get the image file object
        file_obj = context.bot.get_file(file_id)
        # Download the image data
        img_bytes = file_obj.download_as_bytearray()
        # Encrypt the image data
        img_data = bytearray([b ^ 27 for b in img_bytes])
        # Create a Pillow image object
        img = Image.open(BytesIO(img_data))
        # Send the encrypted image
        bio = BytesIO()
        img.save(bio, format="PNG")
        bio.seek(0)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=bio)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please reply to an image with the /en command.")


def decrypt_image(update, context):
    # Check if the reply message is an image
    if update.message.reply_to_message.photo:
        # Get the image file_id
        file_id = update.message.reply_to_message.photo[-1].file_id
        # Get the image file object
        file_obj = context.bot.get_file(file_id)
        # Download the image data
        img_bytes = file_obj.download_as_bytearray()
        # Decrypt the image data
        img_data = bytearray([b ^ 27 for b in img_bytes])
        # Create a Pillow image object
        img = Image.open(BytesIO(img_data))
        # Send the decrypted image
        bio = BytesIO()
        img.save(bio, format="PNG")
        bio.seek(0)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=bio)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please reply to an image with the /dy command.")


def main():
    # Create a Telegram Bot API object
    token = "YOUR_TOKEN_HERE"
    bot = telegram.Bot(token=token)
    # Create a Telegram Bot API updater
    updater = Updater(token=token, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("en", encrypt_image))
    dp.add_handler(CommandHandler("dy", decrypt_image))
    # Start the bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
