import nest_asyncio
nest_asyncio.apply()

import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot's token
TOKEN = "7658978339:AAFhKWLo4B-qZnFthoJXZgnR9kJN7u--5zc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text("Hi there! I'm your bot. How can I help you today?")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def main():
    # Build the application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot until you stop it manually
    await application.run_polling()

if __name__ == '__main__':
    # Run the main() function in the existing event loop
    asyncio.run(main())
