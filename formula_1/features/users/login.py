from datetime import UTC, datetime
from typing import Annotated
import secrets

from fastapi import (
    APIRouter,
    Depends,
    Response,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from formula_1.auth.dependencies import (
    SESSION_EXPIRATION_TIME,
    SESSION_ID_NBYTES,
    SessionDep,
)
from formula_1.db import SessionLocal
from formula_1.db.dependencies import DbSessionDep
from formula_1.db.models import Session, User
from formula_1.features.errors import HTTPExceptionFactory

router = APIRouter()


def authenticate_user(email: str, password: str):
    with SessionLocal() as session:
        user = session.scalars(
            select(User).where(User.email == email)
        ).one_or_none()
    if not user or user.password != password or not user.is_active:
        return None
    return user


@router.post("/login")
def login(
    db: DbSessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
) -> str:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPExceptionFactory.credentials("Incorrect email or password")

    session = Session(
        session_id=secrets.token_urlsafe(SESSION_ID_NBYTES),
        user=user,
        expires_at=datetime.now(UTC) + SESSION_EXPIRATION_TIME,
    )
    db.execute(delete(Session).where(Session.user_id == user.id))
    db.add(session)
    db.commit()
    db.refresh(session)

    # TODO: secure=True para HTTPS/SSL
    response.set_cookie("session_id", session.session_id, httponly=True)
    return "Session issued"


@router.post("/logout")
def logout(db: DbSessionDep, session: SessionDep, response: Response) -> str:
    db.delete(session)
    db.commit()
    response.delete_cookie("session_id")
    return "Session finished"
