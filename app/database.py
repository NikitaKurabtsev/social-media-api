import os
import time

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# from app.utils import FilePrinter, Logger, TerminalPrinter

engine = create_engine(
    f"postgresql"
    f"://{settings.database_username}"
    f":{settings.database_password}"
    f"@{settings.database_hostname}"
    f":{settings.database_port}"
    f"/{settings.database_name}"
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# class DatabaseConnector:
#     """Make postgresql connetion and create cursor object"""
#     @staticmethod
#     def create_connection(logger):
#         while True:
#             try:
#                 connection = psycopg2.connect(
#                     host=os.getenv("HOST"), 
#                     database=os.getenv("DATABASE"), 
#                     user=os.getenv("PSQL_USER"), 
#                     password=os.getenv("PASSWORD"), 
#                     cursor_factory=RealDictCursor
#                 )
#                 cursor = connection.cursor()
#                 logger.log("Succesfull Database connection", FilePrinter)
#                 break

#             except Exception as error:
#                 logger.log(
#                     f"Connecting to Databse failed with error: {error}",
#                     FilePrinter
#                 )
#                 logger.log(
#                     f"Connecting failed, error: {error}",
#                     TerminalPrinter
#                 )
#                 time.sleep(5)
