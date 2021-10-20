from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .connect import CLOUD_DATA_BASE_URL
from loguru import logger
from exception.exceptions import CustomError

engine = create_engine(CLOUD_DATA_BASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

logger.info('Conexión con base de datos: engine = {}', engine)


def get_data_base():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
