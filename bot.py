from click import command, prompt
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

import gpt
from util import *


async def start(update, context):
    dialog.mode = 'main'
    text = load_message("main")
    await send_photo(update, context, name="main")
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        "start": "главное меню бота",
        "profile": "генерация Tinder-профля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос чату GPT 🧠",
    })

async def gpt_command(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, name="gpt")
    await send_text(update, context, text)


async def gpt_dialog(update, context, prompt=None):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)


# usage
async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    else:
        await send_text(update, context, text="Привет")
        await send_text(update, context, text="Как дела?")
        await send_text(update, context, text="Вы написали " + update.message.text)

        await send_photo(update, context, name="avatar_main")
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


dialog = Dialog()
dialog.mode = None

chatgpt = gpt.ChatGptService(token="javcgkAld/r/7U60nS8WDUhWeWVYkZbhjQYpKBFGTvoj5842ast7Pxc54epaCxHRBWXa4vjUutckFaoaUmyOdt62mPPZjjrSFzHlklUvRxjKkD54HiY1iMRLus7TxOkcmPElgqCRPBocX6wJsuWbUTuGkgPNjhYwE08Bvau9oVOiaBcWnUrI/ewY+ccVqx7dnAN4A7RhT46B8BjZjVtU/H8jZakz1cJir+37f/KOL/cTVnmJo=")

app = ApplicationBuilder().token("7591710986:AAFIIae78JOsNeg17dRj1Lt1vHBZePfKvO8").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))

app.run_polling()
