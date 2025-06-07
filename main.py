import telegram
import telegram.ext
import asyncio

# Replace with your actual bot token from BotFather
TOKEN = ""

async def start(update, context):
    """Sends a greeting message when the /start command is issued."""
    await update.message.reply_text('Hello! I am your new friend.')

async def main():
    """Starts the bot."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
