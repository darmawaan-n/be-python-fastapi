from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    CHAR,
)
from config.database import Base

# class Customer(Base):
#     __table_name__ = "m_customer"
    
#     id_customer = Column(Integer, primary_key=True, index=True)
#     norek_customer = Column(CHAR(8), nullable=False)
#     nama_customer = Column(String(255), nullable=False)
#     nik_customer = Column(CHAR(16), nullable=False)
#     hp_number_customer = Column(String(50), nullable=False)
#     saldo_customer = Column(Integer, nullable=False)

metadata = MetaData()
Customer = Table(
    'm_customer', metadata,
    Column('id_customer', Integer, primary_key=True, index=True),
    Column('norek_customer', CHAR(8), nullable=False),
    Column('nama_customer', String(255), nullable=False),
    Column('nik_customer', CHAR(16), nullable=False),
    Column('hp_number_customer', String(50), nullable=False),
    Column('saldo_customer', Integer, nullable=False)
)