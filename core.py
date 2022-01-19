import csv
import re
from datetime import datetime
from string import ascii_lowercase
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date,  DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Float
from databases import databases_config
import app_logger

logger = app_logger.get_logger(__name__)
engine = create_engine(databases_config['basic_db'])
Base = declarative_base()
session = sessionmaker(bind=engine)
session = session()


class Worker(Base):
    """
    класс "Работник", каждый экземляр класса содержит информацию
    об отдельном работнике
    """
    __tablename__ = 'workers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False)
    chat_id = Column(String(50), nullable=True)
    salary = Column(Float(50), nullable=False)
    deployment_date = Column(Date(), nullable=False)
    birthday = Column(Date(), nullable=False)
    status = Column(Boolean, nullable=False)
    schedule = relationship("Schedule", backref="worker", cascade="all,delete")
    requests = relationship("Requests", backref="worker", cascade="all,delete")

    def __str__(self):
        return (f'{self.id}, {self.name}, {self.surname}, {self.patronymic}, '
                f'{self.username}, {self.chat_id}, {self.salary}, {self.deployment_date}, '
                f'{self.birthday}, {self.status}')


class Schedule(Base):
    """
    класс "График работы", каждый экземляр класса содержит информацию
    о графике работы одного работника в одном месяце
    """
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    month = Column(String(50), nullable=False)
    year = Column(String(50), nullable=False)
    d1 = Column(String(50), nullable=True)
    d2 = Column(String(50), nullable=True)
    d3 = Column(String(50), nullable=True)
    d4 = Column(String(50), nullable=True)
    d5 = Column(String(50), nullable=True)
    d6 = Column(String(50), nullable=True)
    d7 = Column(String(50), nullable=True)
    d8 = Column(String(50), nullable=True)
    d9 = Column(String(50), nullable=True)
    d10 = Column(String(50), nullable=True)
    d11 = Column(String(50), nullable=True)
    d12 = Column(String(50), nullable=True)
    d13 = Column(String(50), nullable=True)
    d14 = Column(String(50), nullable=True)
    d15 = Column(String(50), nullable=True)
    d16 = Column(String(50), nullable=True)
    d17 = Column(String(50), nullable=True)
    d18 = Column(String(50), nullable=True)
    d19 = Column(String(50), nullable=True)
    d20 = Column(String(50), nullable=True)
    d21 = Column(String(50), nullable=True)
    d22 = Column(String(50), nullable=True)
    d23 = Column(String(50), nullable=True)
    d24 = Column(String(50), nullable=True)
    d25 = Column(String(50), nullable=True)
    d26 = Column(String(50), nullable=True)
    d27 = Column(String(50), nullable=True)
    d28 = Column(String(50), nullable=True)
    d29 = Column(String(50), nullable=True)
    d30 = Column(String(50), nullable=True)
    d31 = Column(String(50), nullable=True)
    hours = Column(Float(50), nullable=True)
    wage = Column(Float(50), nullable=True)
    worker_id = Column(Integer, ForeignKey('workers.id'))


class Requests(Base):
    """
    Класс, который представляет запросы сотрудников
    на изготовление копии трудовой книжки.
    Каждый экземляр - отдельный запрос суотрудника
    """
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime(), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id'))


class CsvReader:
    """
    Предназначен для чтения данных из CSV файла
    """
    pass

    @staticmethod
    def read_file(path):
        """
        Читает данные из CSV файла, возвращает данные в виде словаря
        """
        try:
            with open(path, 'r', newline='') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')
                result = list(reader)
        except TypeError:
            logger.error(f'админ не указал путь к файлу')
            return None
        else:
            logger.info(f'Осуществлено чтение данных из файла {path}')
            return result


class CsvWriter:
    """
    Предназначен для записи данных в CSV файл
    """
    pass

    @staticmethod
    def write_worker(path, workers_list):
        """
        Записывает всех работников в указанный файл CSV
        :param path: путь к файлу, в кот необходимо произвести запись
        :param workers_list: список, каждый элемент списка
        содержит информацию об отдельном сотруднике
        в виде словаря
        :return возвращает сообщение об ошибке, если возникла ошибка
        """
        if path is None:
            logger.info('администратор не указал путь к файлу')
            return None
        else:
            headers = ['id', 'name', 'surname', 'patronymic', 'username',
                       'salary', 'deployment_date', 'birthday', 'status', 'chat_id']
            for item in workers_list:
                item['salary'] = str(item['salary']).replace('.', ',')
            try:
                with open(path, "w", newline="") as csv_file:
                    writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(workers_list)
            except PermissionError:
                message = (f'запись в файл не была осуществлена, т.к. файл {path} был открыт,'
                           ' закроте файл и повторите попытку')
                logger.error(f'запись в файл не была осуществлена, '
                             f'т.к. файл {path} был открыт')
                return message
            else:
                message = f'была осуществлена запись таблицы "workers" в файл {path}'
                logger.info(f'была осуществлена запись таблицы "workers" в файл {path}')
                return message

    @staticmethod
    def write_schedules(path, schedules_list):
        """
        Записывает все строки из таблицы "schedule" в указанный файл CSV
        :param path: путь к файлу, в кот необходимо произвести запись
        :param schedules_list: список, каждый элемент которого
        содержит информацию о графике работы сотрудника в отдельном месяце
        в виде словаря
        :return: возвращает сообщение об ошибке, если возникла ошибка
        """
        if path is None:
            logger.info('администратор не указал путь к файлу')
            return None
        else:
            headers = ['worker_id', 'month', 'year', 'd1', 'd2', 'd3', 'd4', 'd5',
                       'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13', 'd14',
                       'd15', 'd16', 'd17', 'd18', 'd19', 'd20', 'd21', 'd22', 'd23',
                       'd24', 'd25', 'd26', 'd27', 'd28', 'd29', 'd30', 'd31', 'wage',
                       'hours', 'id']
            for item in schedules_list:
                item['wage'] = str(item['wage']).replace('.', ',')
            try:
                with open(path, "w", newline="") as csv_file:
                    writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(schedules_list)
            except PermissionError:
                message = (f'запись в файл не была осуществлена, т.к. файл {path} был открыт,'
                           ' закроте файл и повторите попытку')
                logger.error(f'запись в файл не была осуществлена, '
                             f'т.к. файл {path} был открыт')
                return message
            else:
                message = f'была осуществлена запись таблицы "schedule" в файл {path}'
                logger.info(f'была осуществлена запись таблицы "schedule" в файл {path}')
                return message


class DbFormatter:
    """
    форматирует данные для записи в базу данных
    """
    pass

    @staticmethod
    def format_worker(data):
        """
        форматирует данные для записи в БД в таблицу 'workers',
        :param data: словарь, каждый элемент кот содержит инф об 1 сотруднике
        :return:
        1) кортеж сообщений, если данные в data не соответсвуют формату БД
        2) список корректных данных, если данные в data соответствуют формату БД
        """
        if data is None:
            return None
        elif not data:
            message = ('структура данных в файле не соответсвует требованиям, либо файл пустой',)
            return message
        else:
            warnings = []
            result = []
            today = datetime.now().date()
            date_sample = r'^\d{2}.\d{2}.\d{4}$'
            usname_sample = ascii_lowercase + '0123456789_'
            for element in data:
                row = {}
                for key, value in element.items():
                    if key == 'patronymic':
                        if value == '':
                            row[key] = value
                        elif not (value.isalpha() and value[0].isupper()):
                            message = (f'указанное {key} "{value}" не корректно'
                                       f'(отчество должно начинаться с заглавной буквы '
                                       f'и должно состоять только из букв)')
                            warnings.append(message)
                        else:
                            row[key] = value
                    elif key == 'name' or key == 'surname':
                        if not (value.isalpha() and value[0].isupper()):
                            message = (f'указанное {key} "{value}" не корректно'
                                       '(имя/фамилия должны начинаться с заглавной буквы, '
                                       'должны состоять только из букв и не могут быть пустой строкой)')
                            warnings.append(message)
                        else:
                            row[key] = value
                    elif key == 'birthday' or key == 'deployment_date':
                        if re.match(date_sample, value) is None:
                            message = f'не корректный формат даты: "{value}"(корректный формат: 01.01.1988)'
                            warnings.append(message)
                        else:
                            try:
                                datetime.strptime(value, "%d.%m.%Y")
                            except ValueError:
                                message = f'не корректный формат даты: "{value}"(не существующая дата)'
                                warnings.append(message)
                            else:
                                if datetime.strptime(value, "%d.%m.%Y").date() > today:
                                    message = f'не корректный формат даты: "{value}"(дата больше текущей)'
                                    warnings.append(message)
                                else:
                                    row[key] = datetime.strptime(value, "%d.%m.%Y").date()
                    elif key == 'username':
                        if len(value) < 5:
                            message = (f'не корректный формат username: "{value}"'
                                       f'({key} должно cостоять из латинских букв. '
                                       'Количество знаков - минимум 5. '
                                       'Возможно применять нижнее подчеркивание и цифры)')
                            warnings.append(message)
                        elif [x for x in value if x not in usname_sample]:
                            message = (f'не корректный формат username: "{value}"'
                                       '(username должно cостоять из латинских букв. '
                                       'Количество знаков - минимум 5. '
                                       'Возможно применять нижнее подчеркивание и цифры)')
                            warnings.append(message)
                        else:
                            row[key] = value
                    elif key == 'salary':
                        if value == '':
                            message = f"вы не указали оклад у сотрудника '{element['surname']}'"
                            warnings.append(message)
                        else:
                            new_value = value.replace(',', '.')
                            try:
                                float(new_value)
                            except ValueError:
                                message = (f'не корректный формат оклада: "{value}"'
                                           '(оклад должен быть числом с плавающей запятой'
                                           ' или целым числом)')
                                warnings.append(message)
                            else:
                                row[key] = float(new_value)
                    else:
                        message = f'не корректное название столбца: "{key}"'
                        warnings.append(message)
                result.append(row)
            logger.info("данные из файла не соответствуют формату") if \
                len(warnings) > 0 or data == ''\
                else logger.info("данные соответствуют формату")

            return tuple(warnings) or result

    @staticmethod
    def format_schedule(data, id_list):
        """
        форматирует данные для записи в базу данных в таблицу 'schedule'
        :param data: словарь, содержащий инф о графике работы сотрудников
        :param id_list: список id сотрудников, внесенных в БД
        :return:
        1) кортеж сообщений, если данные в data не соответсвуют формату БД
        2) список корректных данных, если данные в data соответсвуют формату БД
        """
        if data is None:
            return None
        elif not data:
            message = ('структура данных в файле не соответсвует требованиям, либо файл пустой',)
            return message
        else:
            now_year = datetime.now().year
            months = ['январь', 'февраль', 'март',
                      'апрель', 'май', 'июнь',
                      'июль', 'август', 'сентябрь',
                      'октябрь', 'ноябрь', 'декабрь']
            errors = []
            result = []
            sample = '^[0-2][0-9]:[0-5][0-9]-[0-2][0-9]:[0-5][0-9]$'
            year_sample = '^20[0-9][0-9]$'
            for element in data:
                work_hours = 0
                row = {}
                for key, value in element.items():
                    if key == 'worker_id':
                        if value not in id_list:
                            message = (f'не корректное значение id: "{value}"'
                                       f'(работник c таким id в базе не зарегистрирован)')
                            errors.append(message)
                        else:
                            row[key] = int(value)
                    elif key == 'month':
                        if value in months:
                            row[key] = value
                        else:
                            message = f'не корректное название месяца: "{value}"'
                            errors.append(message)
                    elif key == 'year':
                        if re.match(year_sample, value) is None:
                            message = (f'не корректное значение года: "{value}"'
                                       f'(год должен быть в формате "2020"'
                                       f' и не может быть пустой строкой)')
                            errors.append(message)
                        elif int(value) > now_year:
                            message = f'указан не корректный год: "{value}"(больше текущего)'
                            errors.append(message)
                        else:
                            row[key] = value
                    elif key == 'wage':
                        if value == '':
                            row[key] = 0
                        else:
                            new_value = value.replace(',', '.')
                            try:
                                float(new_value)
                            except ValueError:
                                message = (f'не корректный формат зарплаты: "{value}"'
                                           '(заплата должна быть целым числом, либо '
                                           'числом с плавающей запятой)')
                                errors.append(message)
                            else:
                                row[key] = float(new_value)
                    elif re.match('^d[1-9][0-9]?$', key) is not None and \
                            int(re.findall('[1-9][0-9]?', key)[0]) < 32:
                        if value == '':
                            row[key] = value
                        elif re.match(sample, value) is None:
                            message = (f'не корректный формат времени смены "{value}"'
                                       '(корректный формат: "09:00-18:00")')
                            errors.append(message)
                        else:
                            starth, startm, endh, endm = re.findall(r'\d{2}', value)
                            try:
                                start = datetime(year=1, month=1, day=1, hour=int(starth), minute=int(startm))
                                end = datetime(year=1, month=1, day=1, hour=int(endh), minute=int(endm))
                            except ValueError:
                                message = (f'не корректный формат времени смены "{value}"'
                                           '(кол-во часов должно быть меньше 24)')
                                errors.append(message)
                            else:
                                if end <= start:
                                    message = (f'не корректный формат времени смены "{value}"'
                                               '(время окончания смены не может быть меньше времени ее начала)')
                                    errors.append(message)
                                else:
                                    delta = end - start
                                    work_hours += delta.seconds / 3600 - 1
                                    row[key] = value
                                    row['hours'] = work_hours
                    elif key == 'surname' or key == 'name':
                        pass
                    else:
                        message = f'лишний столбец в шаблоне : "{key}"'
                        errors.append(message)
                result.append(row)
            logger.info("данные из файла не соответствуют формату") if \
                len(errors) > 0 or data == '' \
                else logger.info("данные соответствуют формату")

            return tuple(errors) or result


class DbWriter:
    """
    записывает данные в БД
    """
    pass

    @staticmethod
    def write_worker_db(data, session_name=session):
        """
        Записывает данные из списка data в БД в таблицу 'workers'
        :param data: - список сотрудников, которых необходимо
        записать в БД, каждый элемент списка - словарь,
        содержащий инф-цию об отдельном сотруднике
        :param session_name: имя сессии
        :return: None
        """
        if not data:
            pass
        else:
            for item in data:
                worker = Worker(name=item['name'], surname=item['surname'],
                                patronymic=item['patronymic'], username=item['username'],
                                chat_id='', salary=item['salary'],
                                deployment_date=item['deployment_date'], birthday=item['birthday'],
                                status=True)
                session_name.add(worker)
            session_name.commit()
            logger.info('произведена запись данных в таблицу "workers" в БД')

    @staticmethod
    def write_schedule_db(data, session_name=session):
        """
        Записывает данные из списка data в БД в таблицу 'schedule'
        :param data: - список графиков, которые необходимо
        записать в БД, каждый элемент списка - словарь,
        содержащий инф-цию о графике работы отдельного сотрудника в
        отдельном месяце
        :param session_name: имя сессии
        :return: None
        """
        if not data:
            pass
        else:
            for item in data:
                schedule = Schedule(month=item['month'], year=item['year'],
                                    d1=item['d1'], d2=item['d2'], d3=item['d3'],
                                    d4=item['d4'], d5=item['d5'], d6=item['d6'],
                                    d7=item['d7'], d8=item['d8'], d9=item['d9'],
                                    d10=item['d10'], d11=item['d11'], d12=item['d12'],
                                    d13=item['d13'], d14=item['d14'], d15=item['d15'],
                                    d16=item['d16'], d17=item['d17'], d18=item['d18'],
                                    d19=item['d19'], d20=item['d20'], d21=item['d21'],
                                    d22=item['d22'], d23=item['d23'], d24=item['d24'],
                                    d25=item['d25'], d26=item['d26'], d27=item['d27'],
                                    d28=item['d28'], d29=item['d29'], d30=item['d30'],
                                    d31=item['d31'], hours=item['hours'], wage=item['wage'],
                                    worker_id=item['worker_id']
                                    )
                session_name.add(schedule)
            session_name.commit()
            logger.info('произведена запись данных в таблицу "schedule" в БД')

    @staticmethod
    def write_requests_db(username, quantity, users, session_name=session):
        """
        добавляет запрос пользователя на выдачу
        копии ТК в БД в таблицу "requests"
        :param username: username пользователя, который сделал запрос
         в телеграмме(тип - str)
        :param quantity: кол-во копий, указанное пользователем(тип - int)
        :param users: список пользователей из БД
        :param session_name: имя сессии, по умолчанию -
        переменная session из модуля Core
        :return: None
        """
        for user in users:
            if user['username'] == username:
                request = Requests(time=datetime.now(), quantity=int(quantity),
                                   status=False, worker_id=user['id'])
                session_name.add(request)
                session_name.commit()
                logger.info('произведена запись данных в таблицу "requests" в БД')
                break


class DbLoader:
    """
    подгружает данные из БД
    """
    pass

    @staticmethod
    def load_workers_id(session_name=session):
        """
        Подгружает id работников из БД,
        возвращает в виде списка
        """
        id_list = []
        q = session_name.query(Worker)
        for element in q:
            id_list.append(str(element.id))
        logger.info('подгружены id сотрудников из таблицы "workers" БД')
        return id_list

    @staticmethod
    def load_table(class_name, session_name=session):
        """
        Подгружает все строки из таблицы в БД,
        которая соответсвует указанному классу class_name
        :param class_name: название класса
        :param session_name: имя сессии, по умолчанию -
        переменная session из модуля Core
        :return: список, каждый элемент списка
        содержит словарь с информацией об
        отдельной строке таблицы(тип -list)
        """
        q = session_name.query(class_name)
        result = []
        for element in q:
            item = vars(element)
            del item['_sa_instance_state']
            result.append(item)
        logger.info(f'подгружена таблица {class_name} из БД')
        return result

    @staticmethod
    def load_months(username=None, session_name=session):
        """
        Подгружает столбцы "month" и "year" из таблицы "schedule" БД для
        всех всех работников, если параметр username, не указан,
        либо только для работника, у которого значение поля "username"
        равно значению аргумента username, если аргумент username был указан
        :param username: - username работника в телеграмме(тип - str)
        :param session_name: имя сессии, по умолчанию -
        переменная session из модуля Core
        :return: список кортежей, каждый кортеж состоит из 2 элементов:
        1-название месяца, 2-год, соответствующий месяцу
        """
        result_list = []
        q = session_name.query(Schedule)
        if username is None:
            for element in q:
                row = (element.month, element.year)
                if row not in result_list:
                    result_list.append(row)
            logger.info('подгружены столбцы "month" и "year" из таблицы "schedule" БД')
            sorted_result = (sorted(result_list, key=lambda x: x[1], reverse=True))
        else:
            for element in q:
                if element.worker.username == username:
                    row = (element.month, element.year)
                    if row not in result_list:
                        result_list.append(row)
            logger.info(f'подгружены столбцы "month" и "year" для пользователя '
                        f'{username} из таблицы "schedule" БД')
            sorted_result = (sorted(result_list, key=lambda x: x[1], reverse=True))

        return sorted_result

    @staticmethod
    def load_workers(session_name=session):
        """
        Подгружает столбцы "id", "surname", "name" из таблицы "workers" из БД'
        для всех работников
        :param session_name: имя сессии, по умолчанию -
        переменная session из модуля Core
        :return: список кортежей, каждый элемент кортежа
        содержит инф-цию об отдельном работнике
        """
        result_list = []
        q = session_name.query(Worker)
        for element in q:
            row = (element.id, element.surname, element.name)
            result_list.append(row)
        logger.info('подгружены столбцы "id", "surname", '
                    '"name" из таблицы "workers" из БД')
        return result_list

    @staticmethod
    def load_users(inp_status=None, session_name=session):
        """
        подгружает поля "username", "chat_id",
        "status", "id" из таблицы "workers" БД
        :param inp_status: если не указан - подгружаются все пользователи,
        если указан, то подгружаются только те, у кот указанное
        значение аргумента inp_status равно значению
        в поле "status"(тип - Boolean)
        :param session_name: имя сессии, по умолчанию -
        переменная session из модуля Core
        :return: список словарей, каждый словарь - содержит
        информацию об отдельном пользователе
        """
        result_list = []
        if inp_status is None:
            q = session_name.query(Worker)
        else:
            q = session_name.query(Worker).filter(Worker.status == inp_status)
        for element in q:
            row = dict()
            row['username'] = element.username
            row['chat_id'] = element.chat_id
            row['status'] = element.status
            row['id'] = element.id
            result_list.append(row)
        logger.info('подгружены столбцы "username", "chat_id", '
                    '"status", "id" из таблицы "workers" БД')
        return result_list

    @staticmethod
    def load_schedules(username):
        """
        Подгружает из БД график работы пользователя username из таблицы schedule
        все месяцы
        :param username: телеграмм id пользователя(тип str)
        :return: список объектов класса Schedule(тип - list)
        """
        q = session.query(Worker).filter(Worker.username == username)
        logger.info(f'загружены графики работника ID "{q[0].id}" '
                    f'username "{username}" из БД')
        return q[0].schedule

    @staticmethod
    def load_worker(username):
        """
        Подгружает из БД работника с указанным username
        :param username: тип - str
        :return: объект класс Worker
        """
        q = session.query(Worker).filter(Worker.username == username)
        logger.info(f'загружен работник ID "{q[0].id}" '
                    f'username "{username}" из БД')
        return q[0]

    @staticmethod
    def load_requests():
        """
        подгружает из БД не исполненные запросы
        на изготовление копии ТК, поступившие от сотрудников
        :return: список словарей, каждый словарь содержит
        иноформацию о запросе и пользователе, который его сделал
        """
        q = session.query(Worker, Requests).filter(Worker.id == Requests.worker_id)
        result_list = []
        for request in q:
            if not request.Requests.status:
                row = dict()
                row['request_id'] = request.Requests.id
                row['surname'] = request.Worker.surname
                row['name'] = request.Worker.name
                row['quantity'] = request.Requests.quantity
                row['time'] = request.Requests.time.strftime('%H:%M-%d.%m.%Y')
                row['req_status'] = request.Requests.status
                row['username'] = request.Worker.username
                row['chat_id'] = request.Worker.chat_id
                result_list.append(row)
        return sorted(result_list, key=lambda x: x['request_id'])


class DbEraser:
    """
    Предназначен для удаления данных из БД
    """
    pass

    @staticmethod
    def del_schedule(month, year):
        """
        удаляет из таблицы "schedule" БД все строки,
        в которых поле month = введенному значению аргумента month и
        поле year = введенному значению аргумента year
        :param month: название месяца с маленькой буквы в формате str
        :param year: номер года в формате str
        :return: возвращает сообщение об удаленных данных
        """
        session.query(Schedule).filter(Schedule.month.ilike(month),
                                       Schedule.year.ilike(year)).delete(synchronize_session='fetch')
        session.commit()
        message = (f'все строки из таблицы "schedule" в БД, '
                   f'в которых месяц = {month} и год = {year} были удалены')
        logger.info(f'все строки из таблицы "schedule" в БД, '
                    f'в которых месяц = {month} и год = {year} были удалены')
        return message

    @staticmethod
    def del_worker(worker_id):
        """
        удаляет из таблицы "workers" из БД все строки,
        в которых поле id = введенному значению аргумента worker_id,
        :param worker_id: уникальный id сотрудника в БД, тип - int
        :return: возвращает сообщение об удаленных данных
        """
        q = session.query(Worker).filter(Worker.id == worker_id).one()
        session.delete(q)
        session.commit()
        message = f'сотрудник с id {worker_id} был удален из БД'
        logger.info(f'сотрудник с id {worker_id} был удален из БД')
        return message


class DbChanger:
    """
    Предназначен для обновления данных в БД
    """
    pass

    @staticmethod
    def change_status(worker_id, new_value, session_name=session):
        """
        Меняет старое значение в БД в столбце "status" на новое
        :param worker_id: id сотрудника(тип int)
        :param new_value: новое значение(тип Boolean)
        :param session_name: имя сессии, по умолчанию -
        переменная session из модуля Core
        :return: сообщение о произведенных изменениях(тип str)
        """
        q = session_name.query(Worker).filter(Worker.id == worker_id).one()
        q.status = new_value
        session_name.add(q)
        session_name.commit()
        message = f'статус сотрудника с Id "{worker_id}" в БД был изменен на "{new_value}"'
        logger.info(message)
        return message

    @staticmethod
    def change_chat_id(username, chat_id):
        """
        записывает в таблицу "workers" значение аргумента chat_id
        для строки, в которой значение поля "username" = значению
        указанного аргумента username
        :param username: - username пользователя в телеграмме(тип str)
        :param chat_id: - chat.id с пользователем в телеграмме(тип str)
        """
        q = session.query(Worker).filter(Worker.username == username).one()
        q.chat_id = chat_id
        session.add(q)
        session.commit()
        logger.info(f'значение "chat_id" "{chat_id}" было записано для '
                    f'пользователя "{username}" в таблицу "workers" в БД')

    @staticmethod
    def changestatus_request(request_id, new_value):
        """
        изменяет статус заявки сотрудника на выдачу ТК в БД
        :param request_id: список id запросов в БД
        :param new_value: Новое значение(тип Boolean)
        :return: список сообщений для администратора(тип - список)
        """
        messages = []
        for item in request_id:
            q = session.query(Requests).filter(Requests.id == item).one()
            q.status = new_value
            session.add(q)
            message = f'статус запроса с Id "{item}" был изменен на "{new_value}" в БД'
            messages.append(message)
            logger.info(message)
        session.commit()
        return messages


# if __name__ == "__main__":
#     Base.metadata.create_all(engine)
#     Base.metadata.drop_all(engine)





















