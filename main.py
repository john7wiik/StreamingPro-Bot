
import nest_asyncio
nest_asyncio.apply()

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "7919573124:AAGwbJei7ZhoWiehM29LZOt9vem2XxuNkns"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Free Trial", callback_data="trial")],
        [InlineKeyboardButton("💳 Buy Access", callback_data="buy")],
        [InlineKeyboardButton("❓ How to Pay", callback_data="pay")],
        [InlineKeyboardButton("☎️ Support", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to STREAMING PRO\nChoose an option below:", reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user

    if query.data == "trial":
        await query.edit_message_text("🔥 Thanks! Your free trial access will be sent to you shortly.")
        username = f"@{user.username}" if user.username else user.full_name
        await context.bot.send_message(
            chat_id=7190874264,
            text=f"🔥 {username} has requested a free trial."
        )

    elif query.data == "buy":
        await query.edit_message_text("💳 Yearly subscription: $75\nIncludes all channels, movies, and series.")

    elif query.data == "pay":
        await query.edit_message_text("❓ Payment info:\nBTC: bc1q59aagcv5etsavrw4amhlqqt0ptcl45gs3hs6da8er4ayeveqc8rsp7eenx\nETH: 0x6Ee646f72C0a386c62f3599A775037ca362D5872")

    elif query.data == "support":
        await query.edit_message_text("☎️ Contact support via Telegram: @StreamingProTV")

    else:
        await query.edit_message_text("Unknown option")
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running."

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
    
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    keep_alive()
    try:
        asyncio.run(main())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())
