import typing
import sqlalchemy.exc
import interview_app.db.session as session
import logging

logger = logging.getLogger(__name__)


def get_db() -> typing.Generator:
    try:
        db = session.SessionLocal()
        yield db
    except sqlalchemy.exc.OperationalError as exc:
        logger.error("Cannot connect to the database: %s", exc)
    except Exception as e:
        logger.error(e)
    finally:
        db.close()
