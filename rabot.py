import telebot
import app_logger
from botconfig import bot_configuration
from core import DbLoader, DbChanger


logger = app_logger.get_logger(__name__)
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
        logger.info(f'Сообщение "{self.message}" было отформатировано')
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
        в телеграмме, значение - chat.id с пользователем
        """
        for key, value in users_dict.items():
            try:
                bot.send_message(chat_id=value, text=message)
                logger.info(f'Сообщение "{message}" было отправлено '
                            f'пользователю {key} ')

            except telebot.apihelper.ApiTelegramException:
                logger.exception(f'Бот не смог доставить пользователю {key} '
                                 f'сообщение "{message}"')


@bot.message_handler(commands=['start'])
def send_main_menu(message):
    """перехватывает сообщения от пользователя,
    проверяет, авторизован ли пользователь,
    отвечает пользователю"""
    logger.info(f'пользователь"{message.from_user.username}" '
                f'написал боту ссобщение')
    authorization = False
    if not DbLoader.load_users():
        pass
    else:
        for element in DbLoader.load_users():
            if message.from_user.username in element and element[2] is True:
                authorization = True
                if str(message.chat.id) in element:
                    break
                else:
                    DbChanger.change_chat_id(message.from_user.username, message.chat.id)
                    break
            else:
                pass
    if not authorization:
        bot.send_message(message.chat.id, 'Вы не авторизованы, обратитесь к администратору')
        logger.info(f'бот отправил пользователю '
                    f'"{message.from_user.username}" сообщение')
    else:
        inline_keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        btn_schedule = telebot.types.InlineKeyboardButton(text="график работы", callback_data='schedule')
        btn_personalities = telebot.types.InlineKeyboardButton(text="личные данные", callback_data='personalities')
        btn_url = telebot.types.InlineKeyboardButton(text="сайт организации", url='https://www.python.org')
        inline_keyboard.add(btn_schedule, btn_personalities, btn_url)
        bot.send_message(message.chat.id, 'Выберите опцию:', reply_markup=inline_keyboard)
        logger.info(f'бот отправил пользователю '
                    f'"{message.from_user.username}" сообщение')


@bot.callback_query_handler(func=lambda call: True)
def user_answer(call):
    if call.data == 'schedule':



if __name__ == "__main__":
    logger.info(f'Бот запущен')
    bot.infinity_polling()


