from pyrogram import Client, filters
from pyrogram.types import Message
import base64
from io import BytesIO
from PIL import Image

# Enter your Telegram API credentials below
api_id = 16844842
api_hash = "f6b0ceec5535804be7a56ac71d08a5d4"
bot_token = "5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk"

# Create a Pyrogram client instance
app = Client("image_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Start command handler
@app.on_message(filters.command("start"))
def start_command_handler(client: Client, message: Message):
    response_text = "Hi! I can decode and encode images for you. Send me an image and use the /decode or /encode command to get the results."
    message.reply_text(response_text)

# Decode command handler
@app.on_message(filters.command("decode") | filters.command("de"))
async def decode_command_handler(client: Client, message: Message):
    # Get the photo from the message
    photo = message.reply_to_message.photo.file_id

    # Get the photo file from Telegram
    async for file in client.iter_files(photo):
        # Get the bytes from the photo file
        photo_bytes = BytesIO(await file.download_as_bytearray())

        # Load the image from the bytes
        image = Image.open(photo_bytes)

        # Decode the image
        decoded_image_bytes = base64.b64decode(image.getdata())

        # Create a new image from the decoded bytes
        decoded_image = Image.frombytes(image.mode, image.size, decoded_image_bytes)

        # Save the decoded image as bytes
        decoded_image_bytes_io = BytesIO()
        decoded_image.save(decoded_image_bytes_io, format="PNG")
        decoded_image_bytes_io.seek(0)

        # Send the decoded image
        await message.reply_photo(photo=decoded_image_bytes_io)


async def encode_command_handler(client: Client, message: Message):
    # Get the photo from the message
    photo = message.reply_to_message.photo.file_id

    # Get the photo file from Telegram
    photo_file = await client.get_file(photo)

    # Get the bytes from the photo file
    photo_bytes = BytesIO(await client.download_media(photo_file))

    # Load the image from the bytes
    image = Image.open(photo_bytes)

    # Encode the image
    encoded_image_bytes = base64.b64encode(image.tobytes())

    # Create a new image from the encoded bytes
    encoded_image = Image.frombytes(image.mode, image.size, encoded_image_bytes)

    # Save the encoded image as bytes
    encoded_image_bytes_io = BytesIO()
    encoded_image.save(encoded_image_bytes_io, format="PNG")
    encoded_image_bytes_io.seek(0)

    # Send the encoded image
    await message.reply_photo(photo=encoded_image_bytes_io)





# Start the Pyrogram client
app.run()
