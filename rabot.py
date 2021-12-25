import telebot
from botconfig import bot_configuration


bot = telebot.TeleBot(bot_configuration['TOKEN'])
users = {'vinsmazuka': '1712299131',
         'firmamento_89': '1641854395'}


def mass_message(message, users_dict):
    """
    осуществляет массовую рассылку сообщения
    message
    пользователям из словаря unblock_users.
    В словаре unblock_users ключ - username пользователя
    в телеграмме, значение - chat.id с пользователем.
    Функция реализована как рекурсивная, чтобы обойти
    ошибку, связанную с тем, что некоторые пользователи
    могли заблокировать бота, данные пользователи не получат
    сообщение
    """
    for key, value in users_dict.items():
        try:
            bot.send_message(chat_id=value, text=message)
        except telebot.apihelper.ApiTelegramException:
            pass


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.username in list(users.keys()):
        bot.send_message(message.chat.id, 'Приветики, тебя добавили в друзья бота:)')
        users[message.from_user.username] = str(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Вы не авторизованы, обратитесь к Администратору')


if __name__ == "__main__":
    bot.infinity_polling()


