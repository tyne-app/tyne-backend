from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .connect import CLOUD_DATA_BASE_URL
from loguru import logger

engine = create_engine(CLOUD_DATA_BASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

logger.info('Conexión con base de datos: engine = {}', engine)


def get_data_base():
    db = SessionLocal()

    try:
        yield db
    except:
        db.close()
