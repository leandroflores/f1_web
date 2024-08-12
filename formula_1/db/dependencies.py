from fastapi import Depends
from formula_1.db import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated


def _get_db_session():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


DbSessionDep = Annotated[Session, Depends(_get_db_session)]
