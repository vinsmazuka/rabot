import telebot
from botconfig import bot_configuration


bot = telebot.TeleBot(bot_configuration['TOKEN'])
users = {'vinsmazuka': '',
         'firmamento_89': '1641854395'}


def mass_message(message):
    for chat_id in users.values():
        bot.send_message(chat_id=chat_id, text=message)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.username in list(users.keys()):
        bot.send_message(message.chat.id, 'Приветики, тебя добавили в друзья бота:)')
        users[message.from_user.username] = str(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Вы не авторизованы, обратитесь к Администратору')


if __name__ == "__main__":
    bot.infinity_polling()


