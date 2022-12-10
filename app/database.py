import os
import time
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor

from app.utils import FilePrinter, Logger, TerminalPrinter

# SQLALCHEMY_DATABASE_URL = os.getenv("PSQL_URL")

engine = create_engine("postgresql://postgres:prestigio@localhost/social_media_api")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


logger = Logger()


class DatabaseConnector:
    """Make postgresql connetion and create cursor object"""
    @staticmethod
    def create_connection():
        while True:
            try:
                connection = psycopg2.connect(
                    host=os.getenv("HOST"), 
                    database=os.getenv("DATABASE"), 
                    user=os.getenv("PSQL_USER"), 
                    password=os.getenv("PASSWORD"), 
                    cursor_factory=RealDictCursor
                )
                cursor = connection.cursor()
                logger.log("Succesfull Database connection", FilePrinter)
                break

            except Exception as error:
                logger.log(
                    f"Connecting to Databse failed with error: {error}",
                     FilePrinter
                )
                logger.log(
                    f"Connecting failed, error: {error}", 
                    TerminalPrinter
                )
                time.sleep(5)