


import json
import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

DATA_FILE = 'events.json'


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {'events': [], 'votes': {}}
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def add_event(name, description):
    data = load_data()
    event_id = len(data['events']) + 1
    data['events'].append({'id': event_id, 'name': name, 'description': description})
    save_data(data)

def get_events():
    data = load_data()
    return data['events']

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ho I'm gonna help ya manage ur plans! "
        "Try out: /add_event <name> <description>, /list_events or /help."
    )

async def add_event_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.strip()
    parts = message_text.split(' ', 2)
    if len(parts) < 3:
        await update.message.reply_text(
            "How 2 use: /add_event <name> <description>\n"
            "Example: /add_event Party 'A party at 20:00 in the club'"
        )
        return
    name = parts[1]
    description = parts[2]
    add_event(name, description)
    await update.message.reply_text(
        f"✅ Added a new event:\nName: {name}\nDescription: {description}"
    )

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Commands:\n"
        "/start - Starting message\n"
        "/help - Show all the commands\n"
        "/add_event <name> <description> - Add new event\n"
        "/list_events - Show all your events\n"
    )
    await update.message.reply_text(help_text)

async def list_events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    events = get_events()
    if not events:
        await update.message.reply_text("No events in data base.")
        return

    message_lines = ["All existing events:"]
    for event in events:
        line = f"{event['id']}. {event['name']} — {event['description']}"
        message_lines.append(line)

    await update.message.reply_text("\n".join(message_lines))

# Error handler to log exceptions
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main():
    bot_token = '7655713428:AAEX40dv75OiNiwA9UsoKXFAeL6yYn8Na1M' 
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('add_event', add_event_command))
    application.add_handler(CommandHandler('list_events', list_events_command))
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    
    application.add_error_handler(error_handler)

    application.run_polling()

if __name__ == "__main__":
    main()




    