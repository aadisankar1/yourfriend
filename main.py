from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
TOKEN = ""
banned_words = []
async def start(update:Update,context):
    await update.message.reply_text("""
hey this is your friend, 
i am a friendly bot.
made by @aadiv2bot
no user id because of security
i`m ready!!!!!
""")
async def contact(update:Update,context):
    await update.message.reply_text("i am made by a genius but his id is hidden cause of good reasons so please chat in the bot @aadiv2bot")
async def word_detector(update: Update, context) -> None:
    """Checks if a message contains any banned words."""
    user_message = update.message.text
    if user_message: # Ensure the message is text
        # Convert user message to lowercase for case-insensitive checking
        user_message_lower = user_message.lower()

        # Iterate through the list of banned words
        for banned_word in banned_words:
            # Check if the banned word is present anywhere in the user's message
            if banned_word in user_message_lower:
                 try:
                    # Attempt to delete the message
                    await update.message.delete()
                    # Respond *after* deleting the message.
                    # Note: This reply might also get deleted if your bot is fast
                    # or if the user quickly types another banned word.
                    # It's usually better to reply in private or in a log channel
                    # if the intent is to remove the message from the public chat.
                    await context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Hey! Please be kind and avoid using rude words. Your message was removed."
                    )
                    break
                 except Exception as e:
                    # If deletion fails (e.g., no permission, message too old),
                    # the bot will still send a warning.
                    print(f"Error deleting message: {e}")
                    await update.message.reply_text("Hey! Please be kind and avoid using rude words.")
                    break
async def append():
    if not context.args:
        await update.message.reply_text("Please provide a word to append. Usage: /append word")
        return

    word = context.args[0].lower()
    if word in banned_words:
        await update.message.reply_text(f"'{word}' is already in the banned words list.")
    else:
        banned_words.append(word)
        await update.message.reply_text(f"Added '{word}' to the banned words list.")
    
disp = Application.builder().token(TOKEN).build()

disp.add_handler(CommandHandler("start",start))
disp.add_handler(CommandHandler("contact",contact))
disp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, word_detector))


disp.run_polling(poll_interval=3)
