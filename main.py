import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
import asyncio
import logging # Import logging
import random # Import random for jokes

# Import the profanity filter
from profanity_check import predict, predict_prob

# Enable logging for your bot's activities
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Bot Configuration ---
# IMPORTANT: Replace 'YOUR_BOT_TOKEN' with the actual token you get from BotFather
TOKEN = ""

# --- Jokes List ---
# Add your favorite jokes here! The bot will pick one randomly.
JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Did you hear about the highly educated flea? He went to uni-versity!",
    "What do you call a fake noodle? An impasta!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "What's orange and sounds like a parrot? A carrot!",
    "Why don't skeletons fight each other? They don't have the guts!",
    "What do you call a sad strawberry? A blueberry!"
]

# --- Command Handlers ---

async def start(update: Update, context):
    """Sends a welcome message when the /start command is issued."""
    await update.message.reply_text('Hello! I am your new friend. Use /help to see what I can do!')

async def help_command(update: Update, context):
    """Sends a list of available commands when /help is issued."""
    help_message = (
        'Here\'s what I can do:\n'
        '•  `/start`: Get a warm welcome message.\n'
        '•  `/help`: See this list of commands again.\n'
        '•  `/about`: Learn a little more about me.\n'
        '•  `/joke`: Get a random, chuckle-worthy joke!\n\n'
        'Please remember to be respectful with your messages!'
    )
    await update.message.reply_text(help_message, parse_mode='Markdown')

async def about_command(update: Update, context):
    """Sends information about the bot when the /about command is issued."""
    about_message = (
        "👋 Hello there!\n\n"
        "I am a simple Telegram bot designed to respond to specific commands and help maintain a friendly chat environment.\n\n"
        "**My current features include:**\n"
        "•  `/start`: Get a welcome message.\n"
        "•  `/help`: See a list of all commands.\n"
        "•  `/about`: Learn more about me (you just did!).\n"
        "•  `/joke`: Get a random joke for a quick laugh!\n\n"
        "I also monitor messages for inappropriate language using an advanced profanity filter."
    )
    await update.message.reply_text(about_message, parse_mode='Markdown')

async def joke_command(update: Update, context):
    """Sends a random joke when the /joke command is issued."""
    if JOKES: # Check if the joke list is not empty
        selected_joke = random.choice(JOKES)
        await update.message.reply_text(selected_joke)
    else:
        await update.message.reply_text("Oops! I'm all out of jokes right now.")

# --- Message Handler for Profanity ---

async def check_for_banned_words(update: Update, context):
    """Checks if the user's message contains any profanity using the profanity_check library."""
    if update.message and update.message.text:
        user_message = update.message.text
        
        # predict returns a list of 0s and 1s, where 1 means profanity detected
        # We pass the message as a list of strings
        is_profane = predict([user_message])[0] 
        
        if is_profane == 1:
            # You can also get the probability of profanity if you want more fine-grained control
            # profanity_probability = predict_prob([user_message])[0] 
            
            warning_message = (
                f"⚠️ **Warning!** Your message contains language that is not allowed.\n"
                f"Please keep our chat friendly and refrain from using such terms."
            )
            await update.message.reply_text(warning_message, parse_mode='Markdown')
            logger.warning(
                f"Profanity detected from user {update.effective_user.id} ({update.effective_user.full_name}): "
                f"Message: '{user_message}'"
            )
    # If it's not a text message (e.g., a photo, sticker) or empty, just ignore it.
    # If it's a command, it will be handled by the CommandHandlers first.

async def main():
    """Starts the bot and sets up all handlers."""
    application = Application.builder().token(TOKEN).build()

    # Register Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("joke", joke_command))

    # Register Message Handler for Profanity Check
    # This handler processes all TEXT messages that are NOT commands.
    # It must be placed AFTER all CommandHandlers to ensure commands are processed first.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_for_banned_words))

    # Run the bot until you stop it (e.g., by pressing Ctrl-C in the terminal)
    logger.info("Bot started polling...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main())
