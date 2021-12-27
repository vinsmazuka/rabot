import csv
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, sessionmaker
from sqlalchemy import create_engine, Float
import easygui
from rabot import logging


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
    schedule = relationship("Schedule")

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
    duties = Column(String(50), nullable=True)
    wage = Column(Float(50), nullable=True)
    worker_id = Column(Integer, ForeignKey('workers.id'))
    worker = relationship("Worker")

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
            logging.error(f'админ не указал путь к файлу')
        else:
            logging.info(f'Осуществлено чтение данных из файла {path}')
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
        result = []
        for item in data:
            result.append(Worker(name=str(item['name']), surname=str(item['surname']),
                                 patronymic=str(item['patronymic']), username=str(item['username']),
                                 chat_id='', salary=int(item['salary']),
                                 deployment_date=datetime.strptime(item['deployment_date'],
                                                                   "%d.%m.%Y").date(),
                                 birthday=datetime.strptime(item['birthday'], "%d.%m.%Y").date(),
                                 status=True))
        return result


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
        for item in data:
            session.add(item)
        session.commit()


if __name__ == "__main__":
    DbWriter.write_worker(DbFormatter.format_worker
                          (CsvReader.read_file(easygui.fileopenbox
                                               ("укажите путь к файлу"))))























