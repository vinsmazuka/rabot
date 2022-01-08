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
    pass

    @staticmethod
    def format_schedule(schedule):
        """
        форматирует график работы для отправки пользователю
        :param schedule: - объект класса Schedule
        :return: str
        """
        message = (f'{schedule.month}-{schedule.year}:\n'
                   f'1:   {schedule.d1}\n2:   {schedule.d2}\n3:   {schedule.d3}\n'
                   f'4:   {schedule.d4}\n5:   {schedule.d5}\n6:   {schedule.d6}\n'
                   f'7:   {schedule.d7}\n8:   {schedule.d8}\n9:   {schedule.d9}\n'
                   f'10: {schedule.d10}\n11: {schedule.d11}\n12: {schedule.d12}\n'
                   f'13: {schedule.d13}\n14: {schedule.d14}\n15: {schedule.d15}\n'
                   f'16: {schedule.d16}\n17: {schedule.d17}\n18: {schedule.d18}\n'
                   f'19: {schedule.d19}\n20: {schedule.d20}\n21: {schedule.d21}\n'
                   f'22: {schedule.d22}\n23: {schedule.d23}\n24: {schedule.d24}\n'
                   f'25: {schedule.d25}\n26: {schedule.d26}\n27: {schedule.d27}\n'
                   f'28: {schedule.d28}\n29: {schedule.d29}\n30: {schedule.d30}\n'
                   f'31: {schedule.d31}\n'
                   f'отработанные часы: {schedule.hours}\n'
                   f'зарплата: {schedule.wage}')
        logger.info(f'Объект "{schedule}" был отформатирован для отправки пользователю')
        return message


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


def autorize_func(username, chat_id):
    if not DbLoader.load_users():
        return False
    else:
        for element in DbLoader.load_users():
            if username in element and element[2] is True:
                if str(chat_id) in element:
                    return True
                    break
                else:
                    DbChanger.change_chat_id(username, chat_id)
                    return True
                    break


@bot.message_handler(commands=['start'])
def send_main_menu(message):
    """перехватывает сообщения от пользователя,
    проверяет, авторизован ли пользователь,
    отвечает пользователю"""
    logger.info(f'пользователь"{message.from_user.username}" '
                f'написал боту ссобщение')
    authorization = autorize_func(message.from_user.username, message.chat.id)
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
    """
    Перехватывает ответ пользователя из
    функции send_main_menu и обрабатывает его, отправляя
    пользователю ответ
    """
    authorization = autorize_func(call.from_user.username, call.message.chat.id)
    if not authorization:
        bot.send_message(call.message.chat.id, 'Вы не авторизованы, обратитесь к администратору')
        logger.info(f'бот отправил пользователю '
                    f'"{call.from_user.username}" сообщение')
    elif call.data == 'schedule':
        btn_dict = {}
        for i, val in enumerate(DbLoader.load_months(call.from_user.username)):
            inline_keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
            btn_dict['btn' + str(i)] = telebot.types.InlineKeyboardButton(text=f'{val[0]}-{val[1]}',
                                                                          callback_data=f'{val[0]}-{val[1]}')
        try:
            inline_keyboard.add(*btn_dict.values())
            bot.send_message(call.message.chat.id, 'Выберите месяц:', reply_markup=inline_keyboard)
            logger.info(f'бот отправил пользователю '
                        f'"{call.from_user.username}" сообщение')
        except UnboundLocalError:
            bot.send_message(call.message.chat.id, 'У вас нет доступных графиков работы')
            logger.info(f'бот отправил пользователю '
                        f'"{call.from_user.username}" сообщение')
    else:
        try:
            month, year = call.data.split('-')
        except ValueError:
            pass
        else:
            for element in DbLoader.load_schedules(call.from_user.username):
                if element.month == month and element.year == year:
                    bot.send_message(call.message.chat.id,
                                     Formatter.format_schedule(element))
                    logger.info(f'бот отправил пользователю '
                                f'"{call.from_user.username}" сообщение')


if __name__ == "__main__":
    logger.info(f'Бот запущен')
    bot.infinity_polling()



