import telebot
from botconfig import bot_configuration

users = {'vinsmazuka': '1712299131',
         'firmamento_89': '1641854395'}
bot = telebot.TeleBot(bot_configuration['TOKEN'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.username in users:
        bot.reply_to(message, 'Приветики, тебя добавили в друзья бота:)')
        print(message.from_user.username, message.chat.id)
    else:
        bot.reply_to(message, 'Вы не авторизованы, обратитесь к Администратору - Ивлеву :)')


bot.infinity_polling()

