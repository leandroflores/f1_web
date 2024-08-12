from datetime import UTC, datetime
from fastapi import APIRouter, HTTPException, Response, status
from formula_1.auth.dependencies import SessionDep
from formula_1.db import SessionLocal
from formula_1.db.dependencies import DbSessionDep
from pydantic import BaseModel

router = APIRouter()


class OrganizationRead(BaseModel):
    id: int
    name: str


class UserRead(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_admin: bool
    is_master: bool
    companies: list[OrganizationRead] = []


@router.get("/users/me/")
def users_me(
    db: DbSessionDep, session: SessionDep, response: Response
) -> UserRead:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    if session.expires_at < datetime.now(UTC):
        db.delete(session)
        db.commit()
        response.delete_cookie("session_id")
        raise credentials_exception

    return session.user
