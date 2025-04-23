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


async def gpt_dialog(update, context, prompt_text=None):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)


async def date(update, context):
    dialog.mode = "date"
    text = load_message("date")
    await send_photo(update, context, name="date")
    await send_text_buttons(update, context, text, {
        "date_grande": "Ариана Гранде",
        "date_robbie": "Марго Робби",
        "date_zendaya": "Зенде",
        "date_gosling": " Райан Гослинг",
        "date_hardy": "Том Харди"
    })


async def date_dialog(update, context):
    text = update.message.text
    my_message = await  send_text(update, context, "Набирает текст...")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)


async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update, context, query)
    await send_text(update, context,
                    text="Отличный выбор! Пригласите девушку (парня) на свидание за 5 сообщений" + query,
                    parse_mode=ParseMode.HTML)

    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)


async def message(update, context):
    dialog.mode = "message"
    text = load_message("message")
    await send_photo(update, context, name="message")
    await send_text_buttons(update, context, text, {
        "message_next": "Следующее сообщение",
        "message_date": "Пригласить на свидание"
    })
    dialog.list.clear()


async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()
    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)

    my_message = await send_text(
        update,
        context,
        text="ChatGPT думает 🧠 над вариантами ответа..."
    )

    answer = await chatgpt.send_question(prompt, user_chat_history)

    await my_message.edit_text(answer)


async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


async def profile(update, context):
    dialog.mode = "profile"
    text = load_message("profile")
    await send_photo(update, context, name="profile")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "Сколько вам лет?")


async def profile_dialog(update, context):
    text = update.message.text
    dialog.count += 1
    if dialog.count == 1:
        dialog.user["age"] = text
        await send_text(update, context, "Кем вы работаете?")
    elif dialog.count == 2:
        dialog.user["occupation"] = text
        await send_text(update, context, "У вас есть хобби?")
    elif dialog.count == 3:
        dialog.user["hobbi"] = text
        await send_text(update, context, "Что вам не нравиться в людях?")
    elif dialog.count == 4:
        dialog.user["annoys"] = text
        await send_text(update, context, "Цели знакомства?")
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("profile")
        usrer_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, "Чат GPT занимается 🧠 генерацией вашего парофиля...")
        answer = await chatgpt.send_question(prompt, usrer_info)
        await my_message.edit_text(answer)


async def opener(update, context):
    dialog.mode = "opener"
    text = load_message("opener")
    await send_photo(update, context, name="opener")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.count = 0
    await send_text(update, context, "Имя девушки?")


async def opener_dialog(update, context):
    text = update.message.text
    dialog.count += 1

    if dialog.count == 1:
        dialog.user["name"] = text
        await send_text(update, context, "Сколько ей лет?")
    elif dialog.count == 2:
        dialog.user["age"] = text
        await send_text(update, context, "Оцените её внешность: 1 - 10 баллов?")
    elif dialog.count == 3:
        dialog.user["hendsome"] = text
        await send_text(update, context, "Кем она работает?")
    elif dialog.count == 4:
        dialog.user["occupation"] = text
        await send_text(update, context, "Цель знакомства?")
    elif dialog.count == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("opener")
        usrer_info = dialog_user_info_to_str(dialog.user)
        answer = await chatgpt.send_question(prompt, usrer_info)
        await send_text(update, context, answer)


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    elif dialog.mode == "date":
        await date_dialog(update, context)
    elif dialog.mode == "message":
        await message_dialog(update, context)
    elif dialog.mode == "profile":
        await profile_dialog(update, context)
    elif dialog.mode == "opener":
        await opener_dialog(update, context)
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
dialog.list = []
dialog.count = 0
dialog.user = {}

chatgpt = gpt.ChatGptService(
    token="javcgkAld/r/7U60nS8WDUhWeWVYkZbhjQYpKBFGTvoj5842ast7Pxc54epaCxHRBWXa4vjUutckFaoaUmyOdt62mPPZjjrSFzHlklUvRxjKkD54HiY1iMRLus7TxOkcmPElgqCRPBocX6wJsuWbUTuGkgPNjhYwE08Bvau9oVOiaBcWnUrI/ewY+ccVqx7dnAN4A7RhT46B8BjZjVtU/H8jZakz1cJir+37f/KOL/cTVnmJo=")

app = ApplicationBuilder().token("7591710986:AAFIIae78JOsNeg17dRj1Lt1vHBZePfKvO8").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt_command))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("opener", opener))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="^message_.*"))
app.add_handler(CallbackQueryHandler(hello_button))

app.run_polling()
