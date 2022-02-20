from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger
from ..Settings import Settings
from pytz import utc

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.job import Job
from datetime import datetime

_settings_ = Settings()
_connection_string_ = f'postgresql+psycopg2://{_settings_.DATABASE_USER}:{_settings_.DATABASE_PASSWORD}@{_settings_.DATABASE_HOST}/{_settings_.DATABASE_NAME}'
_engine_ = create_engine(_connection_string_)
_session_local_ = sessionmaker(bind=_engine_)
Base = declarative_base()

logger.info('Conexión con base de datos: engine = {}', _engine_)


def get_data_base():
    db = _session_local_()
    try:
        yield db
    finally:
        db.close()



#def say_hello():
#    print('Hello World!')


#scheduler = BackgroundScheduler()
#jobstore = SQLAlchemyJobStore(url=_connection_string_, engine=_engine_, tableschema='tyne')
#scheduler.add_jobstore(jobstore)

#scheduler.add_job(func=say_hello, id='test', replace_existing=True, trigger='interval', seconds=15)
#scheduler.start()
#print(" Se inicio el scheduler")