import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from features import food_features
from urllib.parse import urljoin
import os
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

TOKEN_ID = os.getenv('TOKEN_ID')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Witam człowieku!")

async def dinner_ideas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_url = urljoin(food_features.BASE_URL, "/przepisy/dania-miesne/")
    text = food_features.get_dinner_from_url(start_url)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(query)
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, nie wiem o co chodzi mordo.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN_ID).build()
    
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    dinner_ideas_handler = CommandHandler('dinner_ideas', dinner_ideas)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(dinner_ideas_handler)
    application.add_handler(echo_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
