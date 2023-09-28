from pydantic import BaseModel, Field
from typing import List

# #1
class CustomerSchema(BaseModel):
    # norek_customer: str = Field(default=None, min_length=8, max_length=8)
    nama_customer: str = Field(..., max_length=255)
    nik_customer: str = Field(..., min_length=16, max_length=16)
    hp_number_customer: str = Field(..., max_length=50)
    # saldo_customer: int = Field(default=0)

    class Config:
        orm_mode=True

class Customer(CustomerSchema):
    id_customer: int
    norek_customer: str
    saldo_customer: int

class CustomerInsert(CustomerSchema):
    pass

class CustomerUpdate(BaseModel):
    norek_customer: str = Field(..., min_length=8, max_length=8)
    nominal: int
    
    class Config:
        orm_mode=True
    
class Customers(BaseModel):
    limit: int = Field(default=5)
    offset: int = Field(default=0)
    data: List[Customer]