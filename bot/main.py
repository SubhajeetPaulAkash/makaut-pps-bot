import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import json

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

# loading content
def load_content():
    with open ("data/content.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
content = load_content()

# Button Handaler
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # prevent loading issues

    action = query.data

    if action == "practice":
        day = "day1"

        if day not in content:
            await query.edit_message_text("❌ Content not available...")
            return
        
        data = content[day]
        message = (
            f"🔥 {data.get('hook', '')}\n\n"
            f"🧠 Topic:\n {data.get('title', 'Day1')}\n\n"
            f"📌 Problem:\n{data.get('problem', '')}\n\n"
            f"⏳ Try for 5 mins before checking hints..."
        )

        keyboard = [
            [InlineKeyboardButton("Hint 1", callback_data="hint_0")],
            [InlineKeyboardButton("Hint 2", callback_data="hint_1")],
            [InlineKeyboardButton("Show Code", callback_data="show_code")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message,reply_markup=reply_markup)
    
    elif action == "continue":
        await query.edit_message_text("📅 Resuming your progress...")
    
    elif action == "hint_0":
        await query.reply_text("💡 Hint 1")

    elif action == "hint_1":
        await query.reply_text("💡 Hint 2")

    elif action == "show_code":
        await query.reply_text("🧑‍💻 Code")

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