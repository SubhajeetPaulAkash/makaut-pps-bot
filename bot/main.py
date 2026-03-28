import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


# START Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Practice Daily", callback_data="practice")],
        [InlineKeyboardButton("📅 Continue Progress", callback_data="continue")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    await update.message.reply_text(
        "Welcome to PPS Bot 🔥\nChoose an option:",
        reply_markup=reply_markup,
    )


# Button Handaler
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer  # prevent loading issues

    data = query.data

    if data == "practice":
        await query.edit_message_text("🚀 Starting Day 1 practice...")
    elif data == "continue":
        await query.edit_message_text("📅 Resuming your progress...")

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is not found. Check .env file")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    print("Bot is running...")
    app.run_polling()

if __name__== "__main__":
    main()