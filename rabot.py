from datetime import datetime
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
        message = (f'{schedule.month} {schedule.year}:\n'
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
        logger.info(f'График за {schedule.month} {schedule.year} был отформатирован для отправки пользователю')
        return message

    @staticmethod
    def format_personalities(worker):
        """
        форматирует объект  worker данные для отправки
        персональных данных пользователю
        :param worker: объект класса Worker
        :return: str
        """
        message = (f'ФИО: {worker.surname} {worker.name} {worker.patronymic}\n'
                   f'Дата рождения: {worker.birthday.strftime("%d.%m.%Y")}\n'
                   f'Дата трудоустройства: {worker.deployment_date.strftime("%d.%m.%Y")}\n'
                   f'Оклад: {worker.salary}')
        logger.info(f'Объект "{worker}" был отформатирован для отправки пользователю')
        return message


class Sendler:
    """
    предназначен для рассылки сообщений
    различными методами
    """
    pass

    @staticmethod
    def mass_sending(message_fusers, unblock_users):
        """
        осуществляет массовую рассылку сообщения
        message пользователям из списка unblock_users.
        :param message_fusers: сообщение для пользователей, тип str
        :param unblock_users: список словарей,
        каждый словарь из списка содержит инф пользоветле
        :return: список сообщений для администратора (тип - list)
        """
        message_fadmin = []
        if not unblock_users:
            result = ('Массовая рассылка не удалась, в базе данных нет '
                      'разблокированных пользователей, '
                      'добавьте пользователей в БД, либо разблокируйте имеюшихся')
            logger.info(result)
            message_fadmin.append(result)
        for user in unblock_users:
            try:
                bot.send_message(chat_id=user['chat_id'], text=message_fusers)
                result = (f'Сообщение было отправлено '
                          f'пользователю "{user["username"]}" ')
                logger.info(result)
                message_fadmin.append(result)
            except telebot.apihelper.ApiTelegramException:
                result = (f'Бот не смог доставить пользователю "{user["username"]}" '
                          f'сообщение , вероятно пользователь заблокировал бота')
                logger.exception(result)
                message_fadmin.append(result)
        return message_fadmin


def autorize_func(username, chat_id):
    """
    проверяет, внесен ли пользователь username в БД
    и открыт ли у него к ней доступ
    :param username: username пользователя в телеграмме,
    :param chat_id: chat.id с пользователем в телеграмме
    :return: True, если пользователь есть в БД и ему разрешен доступ /
    False, если пользователя нет в БД или админ заблокировал
    ему доступ(тип - Boolean)
    """
    if not DbLoader.load_users():
        logger.info(f'пользователь"{username}" не прошел авторизацию')
        return False
    else:
        for element in DbLoader.load_users():
            if username in element.values() and element['status'] is True:
                logger.info(f'пользователь"{username}" прошел авторизацию')
                if str(chat_id) == element['chat_id']:
                    return True
                    break
                else:
                    DbChanger.change_chat_id(username, chat_id)
                    return True
                    break
        logger.info(f'пользователь"{username}" не прошел авторизацию')
        return False


@bot.message_handler(commands=['start'])
def send_main_menu(message):
    """перехватывает сообщения от пользователя,
    проверяет, авторизован ли пользователь,
    отвечает пользователю"""
    logger.info(f'пользователь"{message.from_user.username}" '
                f'запросил у бота главное меню')
    authorization = autorize_func(message.from_user.username, message.chat.id)
    if not authorization:
        bot.send_message(message.chat.id, 'Вы не авторизованы, обратитесь к администратору')
        logger.info(f'бот отправил пользователю '
                    f'"{message.from_user.username}" сообщение о том, что он не авторизован')
    else:
        inline_keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
        btn_schedule = telebot.types.InlineKeyboardButton(text="график работы", callback_data='schedule')
        btn_personalities = telebot.types.InlineKeyboardButton(text="личные данные", callback_data='personalities')
        btn_url = telebot.types.InlineKeyboardButton(text="сайт организации", url='https://www.python.org')
        inline_keyboard.add(btn_schedule, btn_personalities, btn_url)
        bot.send_message(message.chat.id, 'Выберите опцию:', reply_markup=inline_keyboard)
        logger.info(f'бот отправил пользователю '
                    f'"{message.from_user.username}" гланое меню')


@bot.callback_query_handler(func=lambda call: True)
def user_answer(call):
    """
    Перехватывает ответ пользователя из
    функции send_main_menu и обрабатывает его, отправляя
    пользователю ответ
    """
    logger.info(f'пользователь "{call.from_user.username}" запросил {call.data}')
    authorization = autorize_func(call.from_user.username, call.message.chat.id)
    if not authorization:
        bot.send_message(call.message.chat.id, 'Вы не авторизованы, обратитесь к администратору')
        logger.info(f'бот отправил пользователю '
                    f'"{call.from_user.username}" сообщение о том, что он не авторизован')
    elif call.data == 'schedule':
        btn_dict = {}
        for i, val in enumerate(DbLoader.load_months(call.from_user.username)):
            inline_keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
            btn_dict['btn' + str(i)] = telebot.types.InlineKeyboardButton(text=f'{val[0]} {val[1]}',
                                                                          callback_data=f'{val[0]} {val[1]}')
        try:
            inline_keyboard.add(*btn_dict.values())
            bot.send_message(call.message.chat.id, 'Выберите месяц:', reply_markup=inline_keyboard)
            logger.info(f'бот отправил пользователю '
                        f'"{call.from_user.username}" меню с выбором месяца')
        except UnboundLocalError:
            bot.send_message(call.message.chat.id, 'У вас нет доступных графиков работы')
            logger.info(f'бот отправил пользователю '
                        f'"{call.from_user.username}" сообщение об отсутсвии по нему '
                        f'доступных графиков работы')
    elif call.data == 'personalities':
        bot.send_message(call.message.chat.id, Formatter.
                         format_personalities(DbLoader.load_worker(call.from_user.username)))
        logger.info(f'бот отправил пользователю '
                    f'"{call.from_user.username}" персональные данные')
    else:
        try:
            month, year = call.data.split(' ')
        except ValueError:
            pass
        else:
            for element in DbLoader.load_schedules(call.from_user.username):
                if element.month == month and element.year == year:
                    bot.send_message(call.message.chat.id,
                                     Formatter.format_schedule(element))
                    logger.info(f'бот отправил пользователю '
                                f'"{call.from_user.username}" график работы за {month} {year}')


if __name__ == "__main__":
    logger.info(f'Бот запущен')
    bot.infinity_polling()



