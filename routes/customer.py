from schemas import customer as cust_schema
from models.customer import Customer
from config.database import conn
from fastapi import APIRouter, Response, status
import random

customer = APIRouter()

# Mengambil data semua Customer dengan membatasinya dengan limit dan offset
@customer.get('/customer/all', response_model=cust_schema.Customers, description='Menampilkan semua data customer')
async def get_all_customer(limit: int = 10, offset: int = 0):
    query = Customer.select().offset(offset).limit(limit)
    data = conn.execute(query).fetchall()
    response = {'limit': limit, 'offset': offset, 'data': data}
    return response

# Mengambil detail data customer berdasarkan id_customer
@customer.get('/customer/{id_customer}', description='Menampilkan data customer rinci berdasarkan id customer')
async def get_customer(id_customer: int):
    response = Response
    query = Customer.select().filter(Customer.c.id_customer == id_customer)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'status': response.status_code, 'message': 'data tidak ditemukan!'}
    response = {"message": f"sukses mengambil data dengan id {id_customer}", "data": list(data)}
    return response

# 
# Endpoint untuk DAFTAR
# Menambahkan data ke dalam database
# 
@customer.post('/daftar', description='Menambahkan data customer ke dalam database')
async def insert_customer(cst: cust_schema.CustomerInsert):
    response = Response
    cek_nik_hp = Customer.select().where(
        (Customer.c.nik_customer == cst.nik_customer) |
        (Customer.c.hp_number_customer == cst.hp_number_customer)
        )
    # print(cek_nik_hp)
    cek_nik_hp = conn.execute(cek_nik_hp).fetchone()
    if cek_nik_hp is not None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'status': response.status_code, 'remark': 'Data sudah ada!'}
    
    norek = None
    while norek == None:
        ba = ['232']
        for _ in range(5):
            x = random.randint(0, 9)
            ba.append(str(x))
        ba = ''.join(ba)
        cek_ba = Customer.select().filter(Customer.c.norek_customer == ba)
        cek_ba = conn.execute(cek_ba).fetchone()
        if cek_ba is None:
            norek = ba

    query = Customer.insert().values(
        nik_customer = cst.nik_customer,
        norek_customer = norek,
        nama_customer = cst.nama_customer,
        hp_number_customer = cst.hp_number_customer,
        saldo_customer = 0
    )
    # print(query)

    conn.execute(query)
    conn.commit()
    response.status_code = status.HTTP_200_OK
    return {'status': response.status_code, 'nomor_rekening': norek}
# 
# Endpoint untuk TABUNG
# Menambahkan saldo customer
# 
@customer.post('/tabung', description='Menambahkan saldo customer')
async def tabung_customer(cst: cust_schema.CustomerUpdate):
    response = Response
    cek_norek = Customer.select().where(Customer.c.norek_customer == cst.norek_customer)
    cek_norek = conn.execute(cek_norek).fetchone()
    if cek_norek is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'status': response.status_code, 'remark': 'Nomor rekening tidak ditemukan!'}
    
    # print(cek_norek.norek_customer)
    saldo_awal = cek_norek.saldo_customer
    saldo_akhir = saldo_awal + cst.nominal
    
    query = Customer.update().where(Customer.c.norek_customer == cst.norek_customer).values(saldo_customer = saldo_akhir)

    conn.execute(query)
    conn.commit()
    response.status_code = status.HTTP_200_OK
    return {'status': response.status_code, 'saldo': saldo_akhir}

# 
# Endpoint untuk TARIK
# Mengurangi saldo customer
# 
@customer.post('/tarik', description='Mengurangi saldo customer')
async def tarik_customer(cst: cust_schema.CustomerUpdate):
    response = Response
    cek_norek = Customer.select().where(Customer.c.norek_customer == cst.norek_customer)
    cek_norek = conn.execute(cek_norek).fetchone()
    if cek_norek is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'status': response.status_code, 'remark': 'Nomor rekening tidak ditemukan!'}
    if cek_norek.saldo_customer < cst.nominal:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'status': response.status_code, 'remark': 'Saldo tidak mencukupi!'}
    
    # print(cek_norek.norek_customer)
    saldo_awal = cek_norek.saldo_customer
    saldo_akhir = saldo_awal - cst.nominal
    
    query = Customer.update().where(Customer.c.norek_customer == cst.norek_customer).values(saldo_customer = saldo_akhir)

    conn.execute(query)
    conn.commit()
    response.status_code = status.HTTP_200_OK
    return {'status': response.status_code, 'saldo': saldo_akhir}

# 
# Endpoint untuk SALDO
# Mengecek jumlah saldo customer
# 
@customer.get('/saldo/{no_rekening}', description='Menampilkan saldo customer nomor rekening')
async def get_saldo_customer(no_rekening: str):
    response = Response
    query = Customer.select().filter(Customer.c.norek_customer == no_rekening)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'status': response.status_code, 'remark': 'data tidak ditemukan!'}
    response.status_code = status.HTTP_200_OK
    return {'status': response.status_code, 'saldo': data.saldo_customer}