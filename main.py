import pyrogram
from pyrogram import filters
from PIL import Image
import numpy as np

api_id = 16844842
api_hash = "f6b0ceec5535804be7a56ac71d08a5d4"
bot_token = "5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk"

app = pyrogram.Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def reverse_pixels(image):
    """Reverses the pixel values of an image"""
    return Image.eval(image, lambda x: 255 - x)


def add_noise(image, level=0.1):
    """Adds random noise to the image"""
    arr = np.array(image)
    noise = np.random.rand(*arr.shape) * level
    arr = arr + noise
    arr = np.clip(arr, 0, 255)
    return Image.fromarray(arr.astype('uint8'))


def pixelate(image, factor):
    """Pixelates the image by downscaling and upscaling it"""
    w, h = image.size
    small = image.resize((w // factor, h // factor), resample=Image.BOX)
    return small.resize(image.size, resample=Image.NEAREST)


@app.on_message(filters.command("start"))
def start_command(client, message):
    """Handles the /start command"""
    client.send_message(
        chat_id=message.chat.id,
        text="Hi! Send me an image with the /en command to pixelate it or /dy command to reverse the pixels."
    )


@app.on_message(filters.command("en"))
def en_command(client, message):
    """Handles the /en command"""
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo.file_id
        image_path = client.download_media(photo)
        with Image.open(image_path) as im:
            noisy_im = add_noise(im)
            pixelated_im = pixelate(noisy_im, factor=20)
            pixelated_im.save(image_path)
            message.reply_to_message.reply_photo(photo=image_path)
    else:
        message.reply_text("Please reply to an image with this command.")


@app.on_message(filters.command("dy"))
def dy_command(client, message):
    """Handles the /dy command"""
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo.file_id
        image_path = client.download_media(photo)
        with Image.open(image_path) as im:
            pixelated_im = pixelate(im, factor=20)
            reversed_im = reverse_pixels(pixelated_im)
            reversed_im.save(image_path)
            message.reply_to_message.reply_photo(photo=image_path)
    else:
        message.reply_text("Please reply to an image with this command.")


app.run()
