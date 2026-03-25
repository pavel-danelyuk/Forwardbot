import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHAT_ID = "@sarcasmandcats"
DESTINATION_CHATS = [-1001812849723]


def is_source_chat(chat):
    if isinstance(SOURCE_CHAT_ID, str):
        if chat.username is None:
            return False
        return "@" + chat.username == SOURCE_CHAT_ID

    return chat.id == SOURCE_CHAT_ID


async def forward_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post

    if message is None:
        return

    chat = update.effective_chat

    if not is_source_chat(chat):
        return

    for dest in DESTINATION_CHATS:
        try:
            await context.bot.copy_message(
                chat_id=dest,
                from_chat_id=message.chat_id,
                message_id=message.message_id
            )
        except Exception as e:
            print("Ошибка:", e)


def main():
    if TOKEN is None or TOKEN == "":
        raise ValueError("BOT_TOKEN not set")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_post))
    app.run_polling()


if __name__ == "__main__":
    main()
