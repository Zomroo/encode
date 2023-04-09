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
        pattern = np.array([[3, 0, 2, 1], [1, 2, 0, 3], [2, 3, 1, 0], [0, 1, 3, 2]]) # Define the pattern for shuffling
        pattern_flat = pattern.reshape(-1)
        encrypted_flat_arr = np.zeros_like(flat_arr)
        for i in range(h*w):
            encrypted_flat_arr[i] = flat_arr[i][pattern_flat[i % 16]] # Shuffle the pixels according to the pattern
        encrypted_arr = encrypted_flat_arr.reshape(h, w, c)
        encrypted_img = Image.fromarray(encrypted_arr)
        
        # Send the encrypted image to the user
        buffered = BytesIO()
        encrypted_img.save(buffered, format="JPEG")
        buffered.seek(0)
        bot.send_photo(message.chat.id, photo=buffered)
        
        # Send the user the pattern used for encryption
        bot.reply_to(message, f"The pattern used for encryption is {pattern}. Use this pattern with the /dy command to decrypt the image.")
    except Exception as e:
        bot.reply_to(message, "Error: " + str(e))

# Handler for the /dy command
@bot.message_handler(commands=['dy'])
def decrypt_image(message):
    try:
        # Get the photo and pattern from the message
        photo = message.reply_to_message.photo[-1].file_id
        pattern_str = message.text.split()[-1] # Extract the pattern from the message text
        pattern = np.array([int(x) for x in pattern_str.split(",")]).reshape(3,3) # Convert the pattern string to a numpy array
        file_info = bot.get_file(photo)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Convert the downloaded file to an image
        encrypted_img = Image.open(BytesIO(downloaded_file))
        arr = np.array(encrypted_img)
        
        # Decrypt the image by unshuffling the pixels in the pattern
        h, w, c = arr.shape
        flat_arr = arr.reshape(-1, c)
        decrypted_flat_arr = np.zeros_like(flat_arr)
        for i in range(h):
            for j in range(w):
                for k in range(c):
                    new_i, new_j = np.where(pattern == np.array([i % 3, j % 3])) # Find the indices in the pattern that correspond to the current pixel
                    new_i = new_i[0] + (i // 3) * 3 # Convert the indices to the position of the pixel in the original image
                    new_j = new_j[0] + (j // 3) * 3
                    decrypted_flat_arr[new_i*w+new_j][k] = flat_arr[i*w+j][k] # Copy the pixel value to its new position in the decrypted image
        
        arr = decrypted_flat_arr.reshape(h, w, c)
        
        # Convert the decrypted image to bytes and send it to the user
        decrypted_img = Image.fromarray(arr)
        buffered = BytesIO()
        decrypted_img.save(buffered, format="JPEG")
        buffered.seek(0)
        bot.send_photo(message.chat.id, photo=buffered)
    except Exception as e:
        bot.reply_to(message, "Error: " + str(e))


bot.polling()
