from datetime import UTC, datetime, timedelta

from formula_1.db.dependencies import DbSessionDep
from formula_1.db.models import Session, User
from fastapi import (
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
)
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Annotated

SESSION_EXPIRATION_TIME = timedelta(hours=8)
SESSION_ID_NBYTES = 64
TOKEN_NBYTES = 64


class _UserRead(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    id_admin: bool
    is_master: bool
    session: "_SessionRead"


class _SessionRead(BaseModel):
    session_id: str
    user: _UserRead


def _get_current_session(
    db: DbSessionDep,
    response: Response,
    session_id: Annotated[str | None, Cookie()] = None,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
            "Set-Cookie": (
                "session_id=; Max-Age=0; Path=/; SameSite=lax; "
                "Expires=Thu, 01 Jan 1970 00:00:00 GMT;"
            ),
        },
    )
    if not session_id:
        raise credentials_exception

    session = db.scalars(
        select(Session)
        .where(Session.session_id == session_id)
        .options(joinedload(Session.user))
    ).one_or_none()

    if not session:
        raise credentials_exception

    if session.expires_at < datetime.now(UTC):
        db.delete(session)
        db.commit()
        response.delete_cookie("session_id")
        raise credentials_exception

    session.expires_at = datetime.now(UTC) + SESSION_EXPIRATION_TIME
    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def _get_active_user(
    session: Annotated[_SessionRead, Depends(_get_current_session)],
):
    if not session.user.is_active:
        raise HTTPException(status_code=403, detail="Inactive User")
    return session.user


def _get_admin_user(
    session: Annotated[_SessionRead, Depends(_get_current_session)],
):
    if not (session.user.is_active and session.user.is_admin):
        raise HTTPException(status_code=403, detail="Non-admin User")
    return session.user


SessionDep = Annotated[_SessionRead, Depends(_get_current_session)]
ActiveUserDep = Annotated[User, Depends(_get_active_user)]
AdminUserDep = Annotated[User, Depends(_get_admin_user)]
