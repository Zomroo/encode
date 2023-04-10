import schedule
import time

from code import updater, get_handlers
from reset import reset_handler
from database import Database
from batch import batch_command_handler, done_command_handler, dby_command_handler

# Add handlers for the existing commands
handlers = get_handlers()

# Add the handlers to the dispatcher
for handler in handlers:
    updater.dispatcher.add_handler(handler)

# Add the batch command handlers
updater.dispatcher.add_handler(CommandHandler("batch", batch_command_handler))
updater.dispatcher.add_handler(CommandHandler("done", done_command_handler))
updater.dispatcher.add_handler(CommandHandler("dby", dby_command_handler))

# Add the reset command handler
updater.dispatcher.add_handler(reset_handler)

# Start the bot
updater.start_polling()

# Schedule the database reset
schedule.every().day.at("00:00").do(Database.reset)

while True:
    schedule.run_pending()
    time.sleep(1)
