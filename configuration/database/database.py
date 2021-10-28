from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger
from ..Settings import Settings

settings = Settings()
connection_string = f'postgresql+psycopg2://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}'
engine = create_engine(connection_string)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

logger.info('Conexión con base de datos: engine = {}', engine)


def get_data_base():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        print("connection closed")
