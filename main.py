import os
from PIL import Image
from io import BytesIO
from pyrogram import Client, filters
import random

# Set up the Telegram bot token and name
TOKEN = "5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk"
NAME = "Music"

# Initialize the Pyrogram client
app = Client(
    "my_bot",
    bot_token=TOKEN,
    api_id=16844842,
    api_hash="f6b0ceec5535804be7a56ac71d08a5d4"
    debug=True
)

# Define the /start command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hello! I'm a bot that can encrypt images. To encrypt an image, send me a photo and use the /en command. To decrypt an encrypted image, use the /dy command.")
# Define the /en command
@app.on_message(filters.command("en"))
def encrypt_image(client, message):
    # Check if a photo was sent with the command
    if not message.photo:
        message.reply_text("Please send me a photo to encrypt.")
        return

    # Get the photo with the highest resolution
    photo = message.photo[-1]

    # Download the photo to the server
    photo_file = client.download_media(photo)

    # Load the photo into a PIL Image object
    with Image.open(photo_file) as img:
        # Get the size of the image
        width, height = img.size

        # Create a new PIL Image object to store the scrambled image
        scrambled_img = Image.new(img.mode, img.size)

        # Create a list of pixel coordinates
        pixels = [(x, y) for x in range(width) for y in range(height)]

        # Shuffle the pixel coordinates
        random.shuffle(pixels)

        # Loop through the shuffled pixel coordinates and copy the corresponding pixel from the original image to the scrambled image
        for i, (x, y) in enumerate(pixels):
            scrambled_img.putpixel((x, y), img.getpixel(pixels[i]))

        # Save the scrambled image to a buffer
        buffer = BytesIO()
        scrambled_img.save(buffer, format="JPEG")
        buffer.seek(0)

        # Send the scrambled image back to the user
        message.reply_photo(buffer)

    # Remove the photo file from the server
    os.remove(photo_file)
    
# Define the /dy command
@app.on_message(filters.command("dy"))
def decrypt_image(client, message):
    # Check if a reply message exists
    if not message.reply_to_message:
        message.reply_text("Please reply to an encrypted image to decrypt.")
        return

    # Check if the reply message has a photo
    if not message.reply_to_message.photo:
        message.reply_text("The replied message does not contain an image.")
        return

    # Get the photo with the highest resolution from the reply message
    photo = message.reply_to_message.photo[-1]

    # Download the photo to the server
    photo_file = client.download_media(photo)

    # Load the photo into a PIL Image object
    with Image.open(photo_file) as img:
        # Get the size of the image
        width, height = img.size

        # Create a new PIL Image object to store the decrypted image
        decrypted_img = Image.new(img.mode, img.size)

        # Create a list of pixel coordinates
        pixels = [(x, y) for x in range(width) for y in range(height)]

        # Shuffle the pixel coordinates
        random.shuffle(pixels)

        # Loop through the shuffled pixel coordinates and copy the corresponding pixel from the scrambled image to the decrypted image
        for i, (x, y) in enumerate(pixels):
            decrypted_img.putpixel(pixels[i], img.getpixel((x, y)))

    # Save the decrypted image to a buffer
    buffer = BytesIO()
    decrypted_img.save(buffer, format="JPEG")
    buffer.seek(0)

    # Send the decrypted image back to the user
    message.reply_photo(buffer)

    # Remove the photo file from the server
    os.remove(photo_file)

# Start the bot
app.run()
