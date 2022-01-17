import datetime
from unittest import TestCase
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date,  DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Float
from core import CsvReader, DbFormatter, CsvWriter, DbLoader, DbWriter


test_engine = create_engine("postgresql+psycopg2://postgres:Art1988em@localhost/test_database", echo=True)
Base = declarative_base()
test_session = sessionmaker(bind=test_engine)
test_session = test_session()


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


test_list = [{'name': 'Сергей', 'surname': 'Иванов', 'patronymic': 'Владимирович', 'username': 'tyiorty', 'salary': '24500', 'deployment_date': '01.12.2018', 'birthday': '01.01.1998'}, {'name': 'Ксения', 'surname': 'Корягина', 'patronymic': 'Вальдемировна', 'username': 'firmamento', 'salary': '50000', 'deployment_date': '12.03.2016', 'birthday': '01.01.2001'}]
test_list1 = [{'name': '1', 'surname': '', 'patronymic': '', 'username': 'vins', 'salary': '24500,5', 'deployment_date': '01.12.2040', 'birthday': '01.01.022', '': ''}, {'name': 'К1сения', 'surname': 'акирова', 'patronymic': 'раисовна', 'username': 'firmamento_89', 'salary': '', 'deployment_date': '12.03.2016', 'birthday': '01.01.2001', '': 'dsfds'}, {'name': 'василий', 'surname': 'Котов', 'patronymic': 'Петрович1', 'username': 'ruuuu\\uu', 'salary': 'dgdfg', 'deployment_date': '01.01.2018', 'birthday': '46.01.1998', '': ''}, {'name': '', 'surname': '', 'patronymic': '', 'username': '', 'salary': '5000', 'deployment_date': '', 'birthday': '', '': ''}]
test_list2 = ('указанное name "1" не корректно(имя/фамилия должны начинаться с заглавной буквы, должны состоять только из букв и не могут быть пустой строкой)', 'указанное surname "" не корректно(имя/фамилия должны начинаться с заглавной буквы, должны состоять только из букв и не могут быть пустой строкой)', 'не корректный формат username: "vins"(username должно cостоять из латинских букв. Количество знаков - минимум 5. Возможно применять нижнее подчеркивание и цифры)', 'не корректный формат даты: "01.12.2040"(дата больше текущей)', 'не корректный формат даты: "01.01.022"(корректный формат: 01.01.1988)', 'не корректное название столбца: ""', 'указанное name "К1сения" не корректно(имя/фамилия должны начинаться с заглавной буквы, должны состоять только из букв и не могут быть пустой строкой)', 'указанное surname "акирова" не корректно(имя/фамилия должны начинаться с заглавной буквы, должны состоять только из букв и не могут быть пустой строкой)', 'указанное patronymic "раисовна" не корректно(отчество должно начинаться с заглавной буквы и должно состоять только из букв)', "вы не указали оклад у сотрудника 'акирова'", 'не корректное название столбца: ""', 'указанное name "василий" не корректно(имя/фамилия должны начинаться с заглавной буквы, должны состоять только из букв и не могут быть пустой строкой)', 'указанное patronymic "Петрович1" не корректно(отчество должно начинаться с заглавной буквы и должно состоять только из букв)', 'не корректный формат username: "ruuuu\\uu"(username должно cостоять из латинских букв. Количество знаков - минимум 5. Возможно применять нижнее подчеркивание и цифры)', 'не корректный формат оклада: "dgdfg"(оклад должен быть числом с плавающей запятой или целым числом)', 'не корректный формат даты: "46.01.1998"(не существующая дата)', 'не корректное название столбца: ""', 'указанное name "" не корректно(имя/фамилия должны начинаться с заглавной буквы, должны состоять только из букв и не могут быть пустой строкой)', 'указанное surname "" не корректно(имя/фамилия должны начинаться с заглавной буквы, должны состоять только из букв и не могут быть пустой строкой)', 'не корректный формат username: ""(username должно cостоять из латинских букв. Количество знаков - минимум 5. Возможно применять нижнее подчеркивание и цифры)', 'не корректный формат даты: ""(корректный формат: 01.01.1988)', 'не корректный формат даты: ""(корректный формат: 01.01.1988)', 'не корректное название столбца: ""')
test_list3 = [{'name': 'Сергей', 'surname': 'Яровой', 'patronymic': 'Иванович', 'username': 'vins_fjtyv', 'salary': '24500,5', 'deployment_date': '01.12.2001', 'birthday': '01.01.2000'}, {'name': 'Ксения', 'surname': 'Дроздова', 'patronymic': 'Раисовна', 'username': 'firmamento', 'salary': '35000', 'deployment_date': '12.03.2016', 'birthday': '01.01.2001'}, {'name': 'Василий', 'surname': 'Котов', 'patronymic': 'Петрович', 'username': 'ruuuuuu', 'salary': '15000', 'deployment_date': '01.01.2018', 'birthday': '12.01.1998'}]
test_list4 = [{'name': 'Сергей', 'surname': 'Яровой', 'patronymic': 'Иванович', 'username': 'vins_fjtyv', 'salary': 24500.5, 'deployment_date': datetime.date(2001, 12, 1), 'birthday': datetime.date(2000, 1, 1)}, {'name': 'Ксения', 'surname': 'Дроздова', 'patronymic': 'Раисовна', 'username': 'firmamento', 'salary': 35000.0, 'deployment_date': datetime.date(2016, 3, 12), 'birthday': datetime.date(2001, 1, 1)}, {'name': 'Василий', 'surname': 'Котов', 'patronymic': 'Петрович', 'username': 'ruuuuuu', 'salary': 15000.0, 'deployment_date': datetime.date(2018, 1, 1), 'birthday': datetime.date(1998, 1, 12)}]
test_list5 = [{'month': 'ян/варь', 'year': '22', 'd1': '', 'd2': '', 'd3': '', 'd4': '10:00-25:00', 'd5': '22:00-20:00', 'd6': '10:00-19:00', 'd7': '11:00-20:00', 'd8': '10:00-19:00', 'd9': '', 'd10': '', 'd11': '10:00-19:00', 'd12': '11:00-20:00', 'd13': '10:00-19:00', 'd14': '11:00-20:00', 'd15': '10:00-19:00', 'd16': '', 'd17': '', 'd18': '10:00-19:00', 'd19': '11:00-20:00', 'd20': '10:00-19:00', 'd21': '11:00-20:00', 'd22': '10:00-19:00', 'd23': '', 'd24': '', 'd25': '10:00-19:00', 'd26': '11:00-20:00', 'd27': '10:00-19:00', 'd28': '11:00-20:00', 'd29': '10:00-19:00', 'd30': '', 'd31': '', 'wage': '45300.5', 'worker_id': '1', 'surname': '', 'name': '', 'd46': ''}, {'month': '', 'year': '2045', 'd1': '', 'd2': '', 'd3': '', 'd4': '09:00-18:00', 'd5': '09:00-18:00', 'd6': '09:00-18:00', 'd7': '09:00-18:00', 'd8': '09:00-18:00', 'd9': '', 'd10': '', 'd11': '09:00-18:00', 'd12': '09:00-18:00', 'd13': '09:00-18:00', 'd14': '09:00-18:00', 'd15': '09:00-18:00', 'd16': '', 'd17': '', 'd18': '09:00-18:00', 'd19': '09:00-18:00', 'd20': '09:00-18:00', 'd21': '09:00-18:00', 'd22': '09:00-18:00', 'd23': '', 'd24': '', 'd25': '09:00-18:00', 'd26': '09:00-18:00', 'd27': '09:00-18:00', 'd28': '09:00-18:00', 'd29': '09:00-18:00', 'd30': '', 'd31': '', 'wage': 'jjj', 'worker_id': '6', 'surname': '', 'name': '', 'd46': ''}]
test_list6 = ('не корректное название месяца: "ян/варь"', 'не корректное значение года: "22"(год должен быть в формате "2020" и не может быть пустой строкой)', 'не корректный формат времени смены "10:00-25:00"(кол-во часов должно быть меньше 24)', 'не корректный формат времени смены "22:00-20:00"(время окончания смены не может быть меньше времени ее начала)', 'лишний столбец в шаблоне : "d46"', 'не корректное название месяца: ""', 'указан не корректный год: "2045"(больше текущего)', 'не корректный формат зарплаты: "jjj"(заплата должна быть целым числом, либо числом с плавающей запятой)', 'не корректное значение id: "6"(работник c таким id в базе не зарегистрирован)', 'лишний столбец в шаблоне : "d46"')
test_list7 = [{'month': 'январь', 'year': '2022', 'd1': '', 'd2': '', 'd3': '', 'd4': '10:00-19:00', 'd5': '11:00-20:00', 'd6': '10:00-19:00', 'd7': '11:00-20:00', 'd8': '10:00-19:00', 'd9': '', 'd10': '', 'd11': '10:00-19:00', 'd12': '11:00-20:00', 'd13': '10:00-19:00', 'd14': '11:00-20:00', 'd15': '10:00-19:00', 'd16': '', 'd17': '', 'd18': '10:00-19:00', 'd19': '11:00-20:00', 'd20': '10:00-19:00', 'd21': '11:00-20:00', 'd22': '10:00-19:00', 'd23': '', 'd24': '', 'd25': '10:00-19:00', 'd26': '11:00-20:00', 'd27': '10:00-19:00', 'd28': '11:00-20:00', 'd29': '10:00-19:00', 'd30': '', 'd31': '', 'wage': '45300.5', 'worker_id': '1', 'surname': '', 'name': ''}, {'month': 'январь', 'year': '2022', 'd1': '', 'd2': '', 'd3': '09:00-18:30', 'd4': '09:00-18:00', 'd5': '09:00-18:00', 'd6': '09:00-18:00', 'd7': '09:00-18:00', 'd8': '09:00-18:00', 'd9': '', 'd10': '', 'd11': '09:00-18:00', 'd12': '09:00-18:00', 'd13': '09:00-18:00', 'd14': '09:00-18:00', 'd15': '09:00-18:00', 'd16': '', 'd17': '', 'd18': '09:00-18:00', 'd19': '09:00-18:00', 'd20': '09:00-18:00', 'd21': '09:00-18:00', 'd22': '09:00-18:00', 'd23': '', 'd24': '', 'd25': '09:00-18:00', 'd26': '09:00-18:00', 'd27': '09:00-18:00', 'd28': '09:00-18:00', 'd29': '09:00-18:00', 'd30': '', 'd31': '', 'wage': '', 'worker_id': '2', 'surname': '', 'name': ''}]
test_list8 = [{'month': 'январь', 'year': '2022', 'd1': '', 'd2': '', 'd3': '', 'd4': '10:00-19:00', 'hours': 160.0, 'd5': '11:00-20:00', 'd6': '10:00-19:00', 'd7': '11:00-20:00', 'd8': '10:00-19:00', 'd9': '', 'd10': '', 'd11': '10:00-19:00', 'd12': '11:00-20:00', 'd13': '10:00-19:00', 'd14': '11:00-20:00', 'd15': '10:00-19:00', 'd16': '', 'd17': '', 'd18': '10:00-19:00', 'd19': '11:00-20:00', 'd20': '10:00-19:00', 'd21': '11:00-20:00', 'd22': '10:00-19:00', 'd23': '', 'd24': '', 'd25': '10:00-19:00', 'd26': '11:00-20:00', 'd27': '10:00-19:00', 'd28': '11:00-20:00', 'd29': '10:00-19:00', 'd30': '', 'd31': '', 'wage': 45300.5, 'worker_id': 1}, {'month': 'январь', 'year': '2022', 'd1': '', 'd2': '', 'd3': '09:00-18:30', 'hours': 168.5, 'd4': '09:00-18:00', 'd5': '09:00-18:00', 'd6': '09:00-18:00', 'd7': '09:00-18:00', 'd8': '09:00-18:00', 'd9': '', 'd10': '', 'd11': '09:00-18:00', 'd12': '09:00-18:00', 'd13': '09:00-18:00', 'd14': '09:00-18:00', 'd15': '09:00-18:00', 'd16': '', 'd17': '', 'd18': '09:00-18:00', 'd19': '09:00-18:00', 'd20': '09:00-18:00', 'd21': '09:00-18:00', 'd22': '09:00-18:00', 'd23': '', 'd24': '', 'd25': '09:00-18:00', 'd26': '09:00-18:00', 'd27': '09:00-18:00', 'd28': '09:00-18:00', 'd29': '09:00-18:00', 'd30': '', 'd31': '', 'wage': 0, 'worker_id': 2}]
test_list9 = [{'name': 'Сергей', 'id': 5, 'username': 'vins_fjtyv', 'patronymic': 'Иванович', 'salary': 24500.5, 'birthday': datetime.date(2000, 1, 1), 'surname': 'Яровой', 'chat_id': '', 'deployment_date': datetime.date(2001, 12, 1), 'status': True}, {'name': 'Ксения', 'id': 6, 'username': 'firmamento', 'patronymic': 'Раисовна', 'salary': 35000.0, 'birthday': datetime.date(2001, 1, 1), 'surname': 'Дроздова', 'chat_id': '', 'deployment_date': datetime.date(2016, 3, 12), 'status': True}, {'name': 'Василий', 'id': 7, 'username': 'ruuuuuu', 'patronymic': 'Петрович', 'salary': 15000.0, 'birthday': datetime.date(1998, 1, 12), 'surname': 'Котов', 'chat_id': '', 'deployment_date': datetime.date(2018, 1, 1), 'status': True}]
test_list10 = [{'id': '5', 'name': 'Сергей', 'surname': 'Яровой', 'patronymic': 'Иванович', 'username': 'vins_fjtyv', 'salary': '24500,5', 'deployment_date': '2001-12-01', 'birthday': '2000-01-01', 'status': 'True', 'chat_id': ''}, {'id': '6', 'name': 'Ксения', 'surname': 'Дроздова', 'patronymic': 'Раисовна', 'username': 'firmamento', 'salary': '35000,0', 'deployment_date': '2016-03-12', 'birthday': '2001-01-01', 'status': 'True', 'chat_id': ''}, {'id': '7', 'name': 'Василий', 'surname': 'Котов', 'patronymic': 'Петрович', 'username': 'ruuuuuu', 'salary': '15000,0', 'deployment_date': '2018-01-01', 'birthday': '1998-01-12', 'status': 'True', 'chat_id': ''}]
test_list11 = [{'id': 1, 'd6': '10:00-19:00', 'd14': '11:00-20:00', 'd21': '11:00-20:00', 'd28': '11:00-20:00', 'year': '2022', 'd7': '11:00-20:00', 'd15': '10:00-19:00', 'd22': '10:00-19:00', 'd29': '10:00-19:00', 'd1': '', 'd8': '10:00-19:00', 'd16': '', 'd30': '', 'd31': '', 'd2': '', 'd9': '', 'd17': '', 'd23': '', 'hours': 160.0, 'd3': '', 'd10': '', 'd18': '10:00-19:00', 'd24': '', 'wage': 45300.5, 'd4': '10:00-19:00', 'd11': '10:00-19:00', 'd19': '11:00-20:00', 'd25': '10:00-19:00', 'worker_id': 1, 'd5': '11:00-20:00', 'd12': '11:00-20:00', 'd20': '10:00-19:00', 'd26': '11:00-20:00', 'month': 'январь', 'd13': '10:00-19:00', 'd27': '10:00-19:00'}, {'id': 2, 'd6': '09:00-18:00', 'd14': '09:00-18:00', 'd21': '09:00-18:00', 'd28': '09:00-18:00', 'year': '2022', 'd7': '09:00-18:00', 'd15': '09:00-18:00', 'd22': '09:00-18:00', 'd29': '09:00-18:00', 'd1': '', 'd8': '09:00-18:00', 'd16': '', 'd30': '', 'd31': '', 'd2': '', 'd9': '', 'd17': '', 'd23': '', 'hours': 168.5, 'd3': '09:00-18:30', 'd10': '', 'd18': '09:00-18:00', 'd24': '', 'wage': 25000.5, 'd4': '09:00-18:00', 'd11': '09:00-18:00', 'd19': '09:00-18:00', 'd25': '09:00-18:00', 'worker_id': 2, 'd5': '09:00-18:00', 'd12': '09:00-18:00', 'd20': '09:00-18:00', 'd26': '09:00-18:00', 'month': 'январь', 'd13': '09:00-18:00', 'd27': '09:00-18:00'}]
test_list12 = [{'worker_id': '1', 'month': 'январь', 'year': '2022', 'd1': '', 'd2': '', 'd3': '', 'd4': '10:00-19:00', 'd5': '11:00-20:00', 'd6': '10:00-19:00', 'd7': '11:00-20:00', 'd8': '10:00-19:00', 'd9': '', 'd10': '', 'd11': '10:00-19:00', 'd12': '11:00-20:00', 'd13': '10:00-19:00', 'd14': '11:00-20:00', 'd15': '10:00-19:00', 'd16': '', 'd17': '', 'd18': '10:00-19:00', 'd19': '11:00-20:00', 'd20': '10:00-19:00', 'd21': '11:00-20:00', 'd22': '10:00-19:00', 'd23': '', 'd24': '', 'd25': '10:00-19:00', 'd26': '11:00-20:00', 'd27': '10:00-19:00', 'd28': '11:00-20:00', 'd29': '10:00-19:00', 'd30': '', 'd31': '', 'wage': '45300,5', 'hours': '160.0', 'id': '1'}, {'worker_id': '2', 'month': 'январь', 'year': '2022', 'd1': '', 'd2': '', 'd3': '09:00-18:30', 'd4': '09:00-18:00', 'd5': '09:00-18:00', 'd6': '09:00-18:00', 'd7': '09:00-18:00', 'd8': '09:00-18:00', 'd9': '', 'd10': '', 'd11': '09:00-18:00', 'd12': '09:00-18:00', 'd13': '09:00-18:00', 'd14': '09:00-18:00', 'd15': '09:00-18:00', 'd16': '', 'd17': '', 'd18': '09:00-18:00', 'd19': '09:00-18:00', 'd20': '09:00-18:00', 'd21': '09:00-18:00', 'd22': '09:00-18:00', 'd23': '', 'd24': '', 'd25': '09:00-18:00', 'd26': '09:00-18:00', 'd27': '09:00-18:00', 'd28': '09:00-18:00', 'd29': '09:00-18:00', 'd30': '', 'd31': '', 'wage': '25000,5', 'hours': '168.5', 'id': '2'}]
test_list13 = [{'name': 'Сергей', 'surname': 'Иванов', 'patronymic': 'Владимирович', 'username': 'tyiorty', 'salary': 24500.0, 'deployment_date': datetime.date(2018, 12, 1), 'birthday': datetime.date(1998, 1, 1)}, {'name': 'Ксения', 'surname': 'Корягина', 'patronymic': 'Вальдемировна', 'username': 'firmamento', 'salary': 50000.0, 'deployment_date': datetime.date(2016, 3, 12), 'birthday': datetime.date(2001, 1, 1)}]
test_list14 = [{'surname': 'Иванов', 'name': 'Сергей', 'username': 'tyiorty', 'salary': 24500.0, 'birthday': datetime.date(1998, 1, 1), 'id': 1, 'patronymic': 'Владимирович', 'chat_id': '', 'deployment_date': datetime.date(2018, 12, 1), 'status': True}, {'surname': 'Корягина', 'name': 'Ксения', 'username': 'firmamento', 'salary': 50000.0, 'birthday': datetime.date(2001, 1, 1), 'id': 2, 'patronymic': 'Вальдемировна', 'chat_id': '', 'deployment_date': datetime.date(2016, 3, 12), 'status': True}]
test_list15 = [{'month': 'январь', 'd7': '11:00-20:00', 'd14': '11:00-20:00', 'd22': '10:00-19:00', 'd28': '11:00-20:00', 'year': '2022', 'd8': '10:00-19:00', 'd15': '10:00-19:00', 'd29': '10:00-19:00', 'd31': '', 'd1': '', 'd9': '', 'd16': '', 'd23': '', 'd30': '', 'd2': '', 'd10': '', 'd17': '', 'd24': '', 'hours': 160.0, 'd3': '', 'd11': '10:00-19:00', 'd18': '10:00-19:00', 'd25': '10:00-19:00', 'wage': 45300.5, 'd4': '10:00-19:00', 'd12': '11:00-20:00', 'd19': '11:00-20:00', 'd26': '11:00-20:00', 'worker_id': 1, 'id': 1, 'd5': '11:00-20:00', 'd13': '10:00-19:00', 'd20': '10:00-19:00', 'd27': '10:00-19:00', 'd6': '10:00-19:00', 'd21': '11:00-20:00'}, {'month': 'январь', 'd7': '09:00-18:00', 'd14': '09:00-18:00', 'd22': '09:00-18:00', 'd28': '09:00-18:00', 'year': '2022', 'd8': '09:00-18:00', 'd15': '09:00-18:00', 'd29': '09:00-18:00', 'd31': '', 'd1': '', 'd9': '', 'd16': '', 'd23': '', 'd30': '', 'd2': '', 'd10': '', 'd17': '', 'd24': '', 'hours': 168.5, 'd3': '09:00-18:30', 'd11': '09:00-18:00', 'd18': '09:00-18:00', 'd25': '09:00-18:00', 'wage': 0.0, 'd4': '09:00-18:00', 'd12': '09:00-18:00', 'd19': '09:00-18:00', 'd26': '09:00-18:00', 'worker_id': 2, 'id': 2, 'd5': '09:00-18:00', 'd13': '09:00-18:00', 'd20': '09:00-18:00', 'd27': '09:00-18:00', 'd6': '09:00-18:00', 'd21': '09:00-18:00'}]
Base.metadata.drop_all(test_engine)
Base.metadata.create_all(test_engine)
DbWriter.write_worker_db(test_list13, test_session)
DbWriter.write_schedule_db(test_list8, test_session)


class TestCoreMethods(TestCase):
    def test_read_file(self):
        """
        Проверка корректного чтения из csv файла
        """
        self.assertEqual(CsvReader.read_file('test.csv'), test_list)
        self.assertEqual('', '')

    def test_write_worker(self):
        """
        Проверка корректной записи данных из таблицы "workers" в csv-файл
        """
        CsvWriter.write_worker('test1.csv', test_list9)
        self.assertEqual(test_list10, CsvReader.read_file('test1.csv'))
        self.assertEqual(CsvWriter.write_worker(None, test_list9), None)

    def test_write_schedules(self):
        """
        Проверка корректной записи данных из таблицы "schedule" в csv-файл
        """
        CsvWriter.write_schedules('test2.csv', test_list11)
        self.assertEqual(test_list12, CsvReader.read_file('test2.csv'))
        self.assertEqual(CsvWriter.write_schedules(None, test_list11), None)

    def test_format_worker(self):
        """
        Проверка соответствия данных установленному формату
        для записи в таблицу "workers" в БД
        """
        self.assertEqual(DbFormatter.format_worker(test_list1), test_list2)
        self.assertEqual(DbFormatter.format_worker(test_list3), test_list4)

    def test_format_schedule(self):
        """
        Проверка соответствия данных установленному формату
        для записи в таблицу "schedule" в БД
        """
        self.assertEqual(DbFormatter.format_schedule(test_list5, ['1', '2']), test_list6)
        self.assertEqual(DbFormatter.format_schedule(test_list7, ['1', '2']), test_list8)

    def test_write_worker_db(self):
        """
        Проверка корректного чтения/записи данных в таблицу "workers" БД
        """
        self.assertEqual(DbLoader.load_table(Worker, test_session), test_list14)

    def test_write_schedule_db(self):
        """
        Проверка корректного чтения/записи данных в таблицу "schedule" БД
        """
        self.assertEqual(DbLoader.load_table(Schedule, test_session), test_list15)

    def test_load_workers_id(self):
        """
        Проверка корректной выгрузки списка id сотрудников из
        таблицы "workers" БД
        """
        self.assertEqual(DbLoader.load_workers_id(test_session), ['1', '2'])


# if __name__ == "__main__":
#     Base.metadata.create_all(test_engine)
#     Base.metadata.drop_all(test_engine)




