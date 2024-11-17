import os
from sqlalchemy import URL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv(".env")

DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')
ENDPOINT_ID = os.getenv('ENDPOINT_ID')

connection_string = URL.create(
    'postgresql',
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    database=DATABASE_NAME,
)
connection_string = (
    f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}'
    f'@{DATABASE_HOST}/{DATABASE_NAME}?'
    f'options=endpoint%3D{ENDPOINT_ID}&sslmode=require'
)
engine = create_engine(connection_string, )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
