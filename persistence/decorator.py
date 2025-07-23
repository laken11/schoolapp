from functools import wraps


from functools import wraps

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from persistence.database import get_db

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            result = func(*args, session=session, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    return wrapper

