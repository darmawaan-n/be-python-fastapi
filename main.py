from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.customer import customer
from config.database import conn
# import mysql.connector

application = FastAPI()

def cors_headers(application):
    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
        allow_credentials=True,
    )
    return application

application.include_router(customer)

@application.get("/")
async def root():
    if conn is None:
        return {'message': 'Koneksi gagal'}
    else:
        return {'message': 'CRUD fast-api MySQL', 'Authors': 'NRD'}
