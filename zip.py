from pyrogram import Client, filters
from pyrogram.types import Message
import os
import zipfile
import time

app = Client("my_bot", api_id=16844842, api_hash="f6b0ceec5535804be7a56ac71d08a5d4", bot_token="5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4")

@ app.on_message(filters.command("zip"))
def start_zip(bot, message):
    chat_id = message.chat.id
    
    # ask user to send images
    bot.send_message(chat_id, "Please send me up to 20 images to be zipped.")
    images = []
    
    # get up to 20 images or until user types /done
    for i in range(20):
        message = bot.listen(chat_id)
        if message.text and message.text.lower() == "/done":
            break
        elif message.photo:
            images.append(message.photo.file_id)
        elif i == 19:
            bot.send_message(chat_id, "Maximum number of images reached.")
    
    # check if user sent any images
    if not images:
        bot.send_message(chat_id, "No images were sent.")
        return
    
    # ask user to set password
    bot.send_message(chat_id, "Please set a password for the zip file.")
    message = bot.listen(chat_id, timeout=60)
    if not message.text:
        bot.send_message(chat_id, "Timed out. Zip process aborted.")
        return
    password = message.text
    
    # create the zip file and add images
    zip_filename = "images.zip"
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_id in images:
            file_path = bot.download_media(file_id)
            zipf.write(file_path)
            os.remove(file_path)
    
    # encrypt the zip file with password
    encrypted_zip_filename = "images_encrypted.zip"
    with zipfile.ZipFile(encrypted_zip_filename, "w", zipfile.ZIP_AES) as zipf:
        zipf.setpassword(password.encode())
        zipf.write(zip_filename)
    os.remove(zip_filename)
    
    # send the encrypted zip file to user
    bot.send_document(chat_id, encrypted_zip_filename, caption="Here's your encrypted zip file.")
    os.remove(encrypted_zip_filename)

app.run()
