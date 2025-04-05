import nest_asyncio
nest_asyncio.apply()

import logging
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token and Configuration
TOKEN = "7658978339:AAFhKWLo4B-qZnFthoJXZgnR9kJN7u--5zc"
REQUIRED_CHANNELS = ["@Sketch_F_Links", "@Sketch_F_Links"]
MONETAG_LINK_1 = "https://ptounood.top/4/7773072"
MONETAG_LINK_2 = "https://ptounood.top/4/7755294"
OUTPUT_CHANNEL = "@Sketch_F_Links"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    missing_channels = []

    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["creator", "administrator", "member"]:
                missing_channels.append(channel)
        except Exception as e:
            missing_channels.append(channel)

    if missing_channels:
        channels_str = "\n".join(missing_channels)
        message = (
            "🚫 To use this bot, please join the following channels first:\n"
            f"{channels_str}\n\n"
            "After joining, use /start again."
        )
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("✅ Paste Your Sketchfab Model Link")

# Handle user input
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if "https://sketchfab.com/3d-models" in text:
        context.user_data["model_link"] = text
        context.user_data["link1_time"] = datetime.utcnow()

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Click Link 1", url=MONETAG_LINK_1)],
            [InlineKeyboardButton("➡️ Next", callback_data="next_after_link1")]
        ])
        await update.message.reply_text(
            "Step 1: Click Link 1 & Wait On The Page In Order To Detect The Click (Bot will Auto Detect), then click 'Next'.",
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text("❌ Please paste a valid Sketchfab model link.")

# Handle button callbacks
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "next_after_link1":
        start_time = context.user_data.get("link1_time")
        now = datetime.utcnow()

        if not start_time or (now - start_time).total_seconds() < 20:
            await query.edit_message_text("⏱️ Please Visit Page and wait on the first link before continuing.")
            return

        context.user_data["link2_time"] = datetime.utcnow()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Click Link 2", url=MONETAG_LINK_2)]
        ])
        await query.edit_message_text(
            "✅ Step 1 complete! Now click Link 2 and Stay On The Page.",
            reply_markup=keyboard
        )

        await asyncio.sleep(15)
        send_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Send", callback_data="final_send")]
        ])
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Final step: Click 'Send' to submit your model link.",
            reply_markup=send_keyboard
        )

    elif data == "final_send":
        model_link = context.user_data.get("model_link")
        if model_link:
            await context.bot.send_message(chat_id=OUTPUT_CHANNEL, text=f"📦 New Sketchfab Model:\n{model_link}")
            await query.edit_message_text("✅ Your link has been successfully sent to the channel. @Sketch_F_Links")
        else:
            await query.edit_message_text("❌ Error: No model link found.")

# Main
async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
