import numpy as np
import telebot
from PIL import Image
from io import BytesIO

TOKEN = '5931504207:AAHNzBcYEEX7AD29L0TqWF28axqivgoaKUk'
bot = telebot.TeleBot(TOKEN)

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the image encryption and decryption bot! Send me a photo and use the /en command to encrypt it, or use the /dy command followed by an encrypted photo to decrypt it.")

# Handler for the /en command
@bot.message_handler(commands=['en'])
def encrypt_image(message):
    try:
        # Get the photo from the message
        photo = message.reply_to_message.photo[-1].file_id
        file_info = bot.get_file(photo)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Convert the downloaded file to an image
        img = Image.open(BytesIO(downloaded_file))
        arr = np.array(img)
        
        # Encrypt the image by shuffling the pixels
        h, w, c = arr.shape
        flat_arr = arr.reshape(-1, c)
        random_seed = np.random.randint(1, 100000) # Generate a random seed to use for shuffling
        np.random.seed(random_seed)
        np.random.shuffle(flat_arr)
        arr = flat_arr.reshape(h, w, c)
        encrypted_img = Image.fromarray(arr)
        
        # Send the encrypted image to the user
        buffered = BytesIO()
        encrypted_img.save(buffered, format="JPEG")
        buffered.seek(0)
        bot.send_photo(message.chat.id, photo=buffered)
        
        # Send the user the random seed used for encryption
        bot.reply_to(message, f"The random seed used for encryption is {random_seed}. Use this seed with the /dy command to decrypt the image.")
    except Exception as e:
        bot.reply_to(message, "Error: " + str(e))

# Handler for the /dy command
@bot.message_handler(commands=['dy'])
def decrypt_image(message):
    try:
        # Get the photo and random seed from the message
        photo = message.reply_to_message.photo[-1].file_id
        random_seed = int(message.text.split()[-1]) # Extract the random seed from the message text
        file_info = bot.get_file(photo)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Convert the downloaded file to an image
        encrypted_img = Image.open(BytesIO(downloaded_file))
        arr = np.array(encrypted_img)
        
        # Decrypt the image by unshuffling the pixels
        h, w, c = arr.shape
        flat_arr = arr.reshape(-1, c)
        np.random.seed(random_seed) # Use the same random seed as the encryption algorithm
        unshuffled_arr = np.zeros_like(flat_arr)
        for i, j in enumerate(np.argsort(np.random.random(len(flat_arr)))):
            unshuffled_arr[j] = flat_arr[i]
        arr = unshuffled_arr.reshape(h, w, c)
        
        # Convert the decrypted image to bytes and send it to the user
        decrypted_img = Image.fromarray(arr)
        buffered = BytesIO()
        decrypted_img.save(buffered, format="JPEG")
        buffered.seek(0)
        bot.send_photo(message.chat.id, photo=buffered)
    except Exception as e:
        bot.reply_to(message, "Error: " + str(e))

bot.polling()
