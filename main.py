import os
import nest_asyncio
nest_asyncio.apply()

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

TOKEN = "7919573124:AAGsWqAFD1ICOFu3QwOIPEpw5Xhydlx1yGU"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Free Trial", callback_data="trial")],
        [InlineKeyboardButton("💳 Buy Access", callback_data="buy")],
        [InlineKeyboardButton("📦 Our Offers", callback_data="offers")],
        [InlineKeyboardButton("❓ How to Pay", callback_data="howtopay")],
        [InlineKeyboardButton("☎️ Support", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("✨ *Welcome to STREAMING PRO!* ✨\nEnjoy unlimited access to channels, movies & series — fast, HD, and global!", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user

    if query.data == "trial":
        await query.edit_message_text("🔥 Trial activated! One of our agents will contact you shortly with access.")
        username = f"@{user.username}" if user.username else user.full_name
        await context.bot.send_message(chat_id=7190874264, text=f"🔥 {username} requested a FREE TRIAL.")

    elif query.data == "buy":
        keyboard = [
            [InlineKeyboardButton("1 Month ($15)", callback_data="plan_1m")],
            [InlineKeyboardButton("3 Months ($35)", callback_data="plan_3m")],
            [InlineKeyboardButton("6 Months ($50)", callback_data="plan_6m")],
            [InlineKeyboardButton("1 Year ($75)", callback_data="plan_1y")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("💳 *Select your subscription plan:*", reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data.startswith("plan_"):
        plans = {
            "plan_1m": "1 Month ($15)",
            "plan_3m": "3 Months ($35)",
            "plan_6m": "6 Months ($50)",
            "plan_1y": "1 Year ($75)"
        }
        selected = plans.get(query.data, "Unknown Plan")
        username = f"@{user.username}" if user.username else user.full_name
        await context.bot.send_message(chat_id=7190874264, text=f"🛒 {username} selected: {selected}")

        keyboard = [
            [InlineKeyboardButton("₿ Pay with Bitcoin", callback_data="btc")],
            [InlineKeyboardButton("Ξ Pay with Ethereum", callback_data="eth")],
            [InlineKeyboardButton("⬅️ Back", callback_data="buy")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"✅ *{selected}* selected.\n\nPlease choose your payment method:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif query.data == "btc":
        await query.edit_message_text("₿ *Bitcoin Payment*\n\n`bc1q59aagcv5etsavrw4amhlqqt0ptcl45gs3hs6da8er4ayeveqc8rsp7eenx`\n\n✅ Once payment is done, send your proof via @StreamingProTV", parse_mode="Markdown")

    elif query.data == "eth":
        await query.edit_message_text("Ξ *Ethereum Payment*\n\n`0x6Ee646f72C0a386c62f3599A775037ca362D5872`\n\n✅ Once payment is done, send your proof via @StreamingProTV", parse_mode="Markdown")

    elif query.data == "howtopay":
        await query.edit_message_text("❓ *How to Pay*\n\nWe currently accept payments via:\n- ₿ *Bitcoin (BTC)*\n- Ξ *Ethereum (ETH)*\n\nAfter sending your payment, make sure to send a screenshot or proof of transaction via 👉 @StreamingProTV so we can activate your access.", parse_mode="Markdown")

    elif query.data == "offers":
        await query.edit_message_text(
            "📦 *Our Subscription Plans:*\n\n"
            "✅ *1 Month* — $15\n"
            "✅ *3 Months* — $35\n"
            "✅ *6 Months* — $50\n"
            "✅ *1 Year* — $75 (Best Deal!)\n\n"
            "*All plans include:*\n"
            "• Unlimited channels from all countries\n"
            "• Latest movies & series in HD\n"
            "• Lightning-fast & stable servers\n"
            "• 24/7 support via @StreamingProTV\n\n"
            "💡 *To subscribe, click 'Buy Access' from the main menu!*",
            parse_mode="Markdown"
        )

    elif query.data == "support":
        await query.edit_message_text("☎️ *Need help?*\nOur support team is one message away:\n👉 @StreamingProTV", parse_mode="Markdown")

    elif query.data == "back_to_menu":
        await start(update, context)
    else:
        await query.edit_message_text("⚠️ Unknown option.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    await app.bot.delete_webhook(drop_pending_updates=True)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    print("Bot is running...")
    await app.run_polling()

# Keep-alive for Render
from flask import Flask
from threading import Thread

app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is running."

def run():
    port = int(os.environ.get("PORT", 5000))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    import asyncio
    try:
        asyncio.run(main())
    except RuntimeError:
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())
