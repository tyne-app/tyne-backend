from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .url_config import CLOUD_DATA_BASE_URL

engine = create_engine(CLOUD_DATA_BASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_data_base():
    db = SessionLocal()

    try:
        yield db

    except:
        db.close()
