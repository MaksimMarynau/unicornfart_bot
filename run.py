import logging
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from food import food_features
from unicornfart_utils import configs

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

class CommandManager:
    def __init__(self):
        self.run_command = True

    def check_run_command(func):
        async def wrapper(self, update, context):
            if self.run_command:
                await func(self, update, context)
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Bota zatrzymano.\nUzyj /start, aby uruchomic bota.",
                )
        return wrapper

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.run_command = True
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Witam człowieku!"
        )

    @check_run_command
    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Na razie człowieku!"
        )
        self.run_command = False
        return

    @check_run_command
    async def search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tag_name = (
            "".join(context.args) if len(context.args) < 1 else context.args[0]
        )  # support only 1 query for now
        tag_name = tag_name.lower()
        text = food_features.search_idea(configs.FOOD_PURE_URL, tag_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    @check_run_command
    async def list_categories(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        text = food_features.get_available_categories()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    @check_run_command
    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Sorry, nie wiem o co chodzi."
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(configs.TOKEN_ID).build()

    cm = CommandManager()

    start_handler = CommandHandler("start", cm.start)
    stop_handler = CommandHandler("stop", cm.stop)
    search_handler = CommandHandler("search", cm.search)
    category_info_handler = CommandHandler(
        "list_categories", cm.list_categories
    )
    unknown_handler = MessageHandler(filters.COMMAND, cm.unknown)

    application.add_handlers(
        [
            start_handler,
            stop_handler,
            search_handler,
            category_info_handler,
            unknown_handler,
        ]
    )

    application.run_polling()
