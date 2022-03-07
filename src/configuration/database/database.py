from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from loguru import logger
from src.configuration.Settings import Settings
from contextvars import ContextVar
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

_settings = Settings()
_connection_string = f'postgresql+psycopg2://{_settings.DATABASE_USER}:{_settings.DATABASE_PASSWORD}@{_settings.DATABASE_HOST}/{_settings.DATABASE_NAME}'
_engine = create_engine(_connection_string)
_session_local_ = sessionmaker(bind=_engine)
Base = declarative_base()

logger.info('Conexión con base de datos: engine = {}', _engine)

scheduler = BackgroundScheduler()
jobstore = SQLAlchemyJobStore(url=_connection_string, engine=_engine, tableschema='tyne')
scheduler.add_jobstore(jobstore=jobstore)
scheduler.start() # TODO: Ver una manera de no tener ejecutándose el scheduler siempre
logger.info("jobstore = {}", jobstore)


def get_data_base():
    db = _session_local_()
    try:
        yield db
    finally:
        db.close()


db_session: ContextVar[Session] = ContextVar('db_session')
logger.info("db_session = {}", db_session)