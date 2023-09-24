import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from features import food_features
from urllib.parse import urljoin
import os
from dotenv import load_dotenv
from features import PURE_URL

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

TOKEN_ID = os.getenv('TOKEN_ID')


class CommandManager:
    def __init__(self):
        self.run_command = True

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.run_command = True
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Witam człowieku!")

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.run_command:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Na razie człowieku!")
            self.run_command = False
            return
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Uzyj /start, aby uruchomic bota.")

    async def dinner_ideas(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.run_command:
            start_url = urljoin(PURE_URL, "/przepisy/dania-miesne/")
            text = food_features.get_dinner_from_url(start_url)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    async def ideas_from_tag(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.run_command:
            tag_name = "".join(context.args) if len(context.args) < 1 else context.args[0] # support only 1 tag for now
            tag_name = tag_name.lower()
            text = food_features.get_tag_dishes(PURE_URL, tag_name)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.run_command:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, nie wiem o co chodzi mordo.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN_ID).build()
    
    cm = CommandManager()
    
    start_handler = CommandHandler('start', cm.start)
    stop_handler = CommandHandler('stop', cm.stop)
    tag_handler = CommandHandler('ideas_from_tag', cm.ideas_from_tag)
    dinner_ideas_handler = CommandHandler('dinner_ideas', cm.dinner_ideas)
    unknown_handler = MessageHandler(filters.COMMAND, cm.unknown)
    
    application.add_handlers([start_handler, stop_handler, tag_handler, dinner_ideas_handler, unknown_handler])

    application.run_polling()
