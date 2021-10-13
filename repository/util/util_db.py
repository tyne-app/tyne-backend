def db_persist(func):
    def persist(*args, **kwargs):
        func(*args, **kwargs)
        try:
            session.commit()
            logger.info("success calling db func: " + func.__name__)
            return True
        except SQLAlchemyError as e:
            logger.error(e.args)
            session.rollback()
            return False

    return persist
