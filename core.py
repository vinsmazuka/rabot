from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Float

engine = create_engine("postgresql+psycopg2://postgres:Art1988em@localhost/rabotdb",
                       echo=True)
Base = declarative_base()


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
    status = Column(Boolean, nullable=False)
    schedule = relationship("Schedule")


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





















