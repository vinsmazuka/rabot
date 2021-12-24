from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:Art1988em@localhost/rabotdb")






