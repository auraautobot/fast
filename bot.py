import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.chat_join_request.approve()

async def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    await application.initialize()
    await application.start()
    print("Bot started...")
    await application.updater.start_polling()
    await application.updater.idle()

import asyncio
@app.before_first_request
def start_bot():
    asyncio.create_task(run_bot())

@app.route('/')
def home():
    return "Bot is alive!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
