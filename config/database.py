# import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import configparser

# config = configparser.ConfigParser()
# config.read('alembic.ini')

# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:MYsql_Oman-1996!@localhost:8000/fast_api_python'
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://oman_1996:Oman_1234@localhost:3306/fast_api_python'
SQLALCHEMY_DATABASE_URL = 'postgresql://psqluser:psqlpassword@localhost/fast_api_python'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

conn = engine.connect()