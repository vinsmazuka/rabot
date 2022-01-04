import csv
import re
from datetime import datetime
from string import ascii_lowercase
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Float
import easygui
import app_logger

logger = app_logger.get_logger(__name__)
engine = create_engine("postgresql+psycopg2://postgres:Art1988em@localhost/rabotdb",
                       echo=True)
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
    salary = Column(Integer, nullable=False)
    deployment_date = Column(Date(), nullable=False)
    birthday = Column(Date(), nullable=False)
    status = Column(Boolean, nullable=False)

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
    worker = relationship("Worker", backref="schedules", cascade="all,delete")


# Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)


class CsvReader:
    """
    Предназначен для чиения данных из CSV файла
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
                print(result)
        except TypeError:
            logger.error(f'админ не указал путь к файлу')
            return ''
        else:
            logger.info(f'Осуществлено чтение данных из файла {path}')
            return result


class DbFormatter:
    """
    форматирует данные для записи в базу данных
    """
    pass

    @staticmethod
    def format_worker(data):
        """форматирует данные для записи в базу данных в таблицу 'workers',
        параметр data - словарь, каждый элемент которого преобразуется
        в класс Worker"""
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
                            row[key] = new_value
                else:
                    message = f'не корректное название столбца: "{key}"'
                    warnings.append(message)
            result.append(row)
        logger.info("данные из файла не соответствуют формату") if \
            len(warnings) > 0 else logger.info("данные соответствуют формату")

        return tuple(warnings) if len(warnings) > 0 else result


class DbWriter:
    """
    записывает данные в БД
    """
    pass

    @staticmethod
    def write_worker(data):
        """
        Записывает данные data в БД в таблицу 'workers'
        параметр data - список, каждый элемент которого -
        """
        if not data:
            pass
        else:
            for item in data:
                session.add(item)
            session.commit()


if __name__ == "__main__":
    # DbWriter.write_worker(DbFormatter.format_worker
    #                        (CsvReader.read_file(easygui.fileopenbox
    #                                            ("укажите путь к файлу"))))
    x = DbFormatter.format_worker(CsvReader.read_file(easygui.fileopenbox("укажите путь к файлу")))
    print(x)























