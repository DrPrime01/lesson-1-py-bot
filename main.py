import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables from .local.env file
load_dotenv('.env.local')
bot_username = os.getenv("BOT_USERNAME")
token = os.getenv("TOKEN")

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Welcome to lesson 1 bot. Kindly state your purpose here.")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! What can I do for you?")
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")
    
# Response Handlers
def handle_response(text: str) -> str:
    lowered_text: str = text.lower()
    
    if "hello" in lowered_text:
        return "Hey, there"
    if "how are you" in lowered_text:
        return "I'm good. What about you?"
    if "i love python" in lowered_text:
        return "Same here. Good to know"
    return "I don't understand what you wrote. Can you please be clearer?"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type # tells us if it's a group chat or DM
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in ({message_type}): "{text}"')
    
    if message_type == "group":
        if bot_username in text:
            new_text: str = text.replace(bot_username, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print("Bot: ", response)
    await update.message.reply_text(response)
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(token).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Error
    app.add_error_handler(error)
    
    # Polling interval for checking for messages
    print("Polling...")
    app.run_polling(poll_interval=2.5)