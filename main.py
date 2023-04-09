import pyrogram
from pyrogram import filters
from PIL import Image

api_id = 16844842
api_hash = "f6b0ceec5535804be7a56ac71d08a5d4"
bot_token = "5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk"

app = pyrogram.Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def reverse_pixels(image):
    """Reverses the pixel values of an image"""
    return Image.eval(image, lambda x: 255 - x)


def inverse_pixels(image):
    """Inverses the pixel values of an image"""
    return Image.eval(image, lambda x: 255 ^ x)


@app.on_message(filters.command("start"))
def start_command(client, message):
    """Handles the /start command"""
    client.send_message(
        chat_id=message.chat.id,
        text="Hi! Send me an image with the /en command to reverse the pixels or /dy command to inverse the pixels."
    )


@app.on_message(filters.command("en"))
def en_command(client, message):
    """Handles the /en command"""
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo[-1]
        file = photo.get_file()
        image_path = file.download()
        with Image.open(image_path) as im:
            im = im.convert("L")
            reversed_im = reverse_pixels(im)
            reversed_im.save(image_path)
            message.reply_to_message.reply_photo(photo)
    else:
        message.reply_text("Please reply to an image with this command.")


@app.on_message(filters.command("dy"))
def dy_command(client, message):
    """Handles the /dy command"""
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo[-1]
        file = photo.get_file()
        image_path = file.download()
        with Image.open(image_path) as im:
            im = im.convert("L")
            inverse_im = inverse_pixels(im)
            inverse_im.save(image_path)
            message.reply_to_message.reply_photo(photo)
    else:
        message.reply_text("Please reply to an image with this command.")


app.run()
