import logging
import telebot
from botconfig import bot_configuration

FORMAT = '%(asctime)s - Уровень %(levelname)s в %(filename)s.%(funcName)s: %(message)s'
logging.basicConfig(filename='log.txt', filemode='a', level=logging.INFO, format=FORMAT)

bot = telebot.TeleBot(bot_configuration['TOKEN'])

users = {'vinsmazuka': '1712299131',
         'firmamento_89': '1641854395'}


class Formatter:
    """
    Предназначен для предобразования сообщения
    в необходимы формат перед отправкой
    """
    def __init__(self, message):
        self.message = message

    def form(self):
        logging.info(f'Сообщение "{self.message}" было отформатировано')
        return self.message


class Sendler:
    """
    предназначен для рассылки сообщений
    различными методами
    """
    pass

    @staticmethod
    def mass_sending(message, users_dict):
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
                logging.info(f'Сообщение "{message}" было отправлено '
                             f'пользователю {key} ')
            except telebot.apihelper.ApiTelegramException:
                logging.error(f'Бот не смог доставить пользователю {key} '
                              f'сообщение "{message}"')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.username in list(users.keys()):
        bot.send_message(message.chat.id, 'Приветики, тебя добавили в друзья бота:)')
        users[message.from_user.username] = str(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Вы не авторизованы, обратитесь к Администратору')


if __name__ == "__main__":
    bot.infinity_polling()


