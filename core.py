from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Float

engine = create_engine("postgresql+psycopg2://postgres:Art1988em@localhost/rabotdb")
Base = declarative_base()

class Workers(Base):
    """
    класс Работник, каждый экземляр класса содержит информацию
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
    depl_date = Column(Date(50), nullable=False)


















