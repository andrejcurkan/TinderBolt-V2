from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from gpt import *
from util import *


async def start(update, context):
    text = load_message("main")
    await send_photo(update, context, name="avatar_main")
    await send_text(update, context, text)


# usage
async def hello(update, context):
    await send_text(update, context, text="Привет")
    await send_text(update, context, text="Как дела?")
    await send_text(update, context, text="Вы написали " + update.message.text)

    await send_photo(update, context, name="avatar-main")
    await send_text_buttons(update, context, text="Запустить процесс?", buttons={
        "start": "Запустить",
        "stop": "Остановить"
    })


# usage
async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, text="Процесс запущен")
    else:
        await send_text(update, context, text="Процесс остановлен")


app = ApplicationBuilder().token("7591710986:AAFIIae78JOsNeg17dRj1Lt1vHBZePfKvO8").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))

app.run_polling()
