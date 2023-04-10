from telegram.ext import CommandHandler
from commands import start_command_handler, en_command_handler, dy_command_handler


def get_handlers():
    handlers = [
        CommandHandler("start", start_command_handler),
        CommandHandler("en", en_command_handler),
        CommandHandler("dy", dy_command_handler),
    ]
    return handlers
