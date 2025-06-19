import telebot
import webbrowser

bot = telebot.TeleBot("7649544371:AAFy35g6o6IpT3O-BE-2SkUgK1Rw_tG3rak")
ADMIN_ID = 695020439

current_poll = {
    "question": None,
    "options": []
}


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open_new_tab('https://belaz.by')

    @bot.message_handler()
    def info(message):
        if message.text.lower() == 'привет':
            bot.send_message(message.chat.id,
                             f'Здравствуйте, {message.from_user.first_name} {message.from_user.last_name}')
        elif message.text.lower() == 'id':
            bot.reply_to(message, f'ID: {message.from_user.id}')
        elif message.text.lower() == '/start':
            bot.send_message(message.chat.id,
                             f'Здравствуйте, {message.from_user.first_name} {message.from_user.last_name}')
        elif message.text.lower() == '/help':
            bot.send_message(message.chat.id, f'Данный бот создан для голосований сотрудников БелАЗ.')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}!")

@bot.message_handler(commands=['newpoll'])
def newpoll(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "У вас нет прав на создание опроса.")
        return

    msg = bot.send_message(message.chat.id, "Введите вопрос для опроса:")
    bot.register_next_step_handler(msg, get_question)

def get_question(message):
    current_poll["question"] = message.text
    msg = bot.send_message(message.chat.id, "Введите варианты ответа через запятую (,):")
    bot.register_next_step_handler(msg, get_options)

def get_options(message):
    options = [opt.strip() for opt in message.text.split(",") if opt.strip()]
    if len(options) < 2:
        msg = bot.send_message(message.chat.id, "Введите минимум 2 варианта.")
        bot.register_next_step_handler(msg, get_options)
        return

    current_poll["options"] = options
    bot.send_message(message.chat.id, "Опрос сохранён. Пользователи могут использовать /poll.")

@bot.message_handler(commands=['poll'])
def poll(message):
    if not current_poll["question"]:
        bot.send_message(message.chat.id, "Опрос не создан.")
        return

    bot.send_poll(
        chat_id=message.chat.id,
        question=current_poll["question"],
        options=current_poll["options"],
        is_anonymous=False,
        allows_multiple_answers=False
    )

bot.infinity_polling()
