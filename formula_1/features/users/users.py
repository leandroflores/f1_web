from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import and_, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload

from formula_1.auth.dependencies import ActiveUserDep, AdminUserDep
from formula_1.db import SessionLocal
from formula_1.db.dependencies import DbSessionDep
from formula_1.db.models import Company, User
from formula_1.features.errors import HTTPExceptionFactory
from formula_1.utils import update_object


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CompanyRead(BaseModel):
    id: int


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
    created_at: datetime
    organization: OrganizationRead | None
    companies: list[CompanyRead] = []


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    organization_id: int
    is_active: bool = True
    is_admin: bool = False
    companies_ids: list[int] = []


class UserEdit(BaseModel):
    email: str
    full_name: str
    organization_id: int
    is_active: bool = True
    is_admin: bool = False
    companies_ids: list[int] = []


@router.get("/users")
def list_users(
    request_user: ActiveUserDep,
) -> list[UserRead]:
    if request_user.is_master:
        query = (
            select(User)
            .options(joinedload(User.organization))
            .options(selectinload(User.companies))
            .where(User.is_master == False)
            .order_by(User.full_name.asc())
        )
    elif request_user.is_admin:
        query = (
            select(User)
            .options(joinedload(User.organization))
            .options(selectinload(User.companies))
            .where(
                and_(
                    User.organization_id == request_user.organization_id,
                    User.is_master == False,
                    and_(
                        or_(
                            User.is_admin == False,
                            and_(
                                User.is_admin == True,
                                User.created_by_id == request_user.id
                            )
                        )
                    )
                )
            )
            .order_by(User.full_name.asc())
        )
    else:
        return []
    with SessionLocal() as db_session:
        users = db_session.scalars(query).all()
    return users


@router.post("/users")
def create_user(
    db: DbSessionDep, request_user: ActiveUserDep, data: UserCreate
) -> UserRead:
    new_user = User(
        created_by=request_user,
        **data.model_dump(exclude=["organization_id", "companies_ids"]),
    )

    new_user.organization_id = data.organization_id
    new_user.companies = (
        db.execute(select(Company).where(Company.id.in_(data.companies_ids)))
        .scalars()
        .all()
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPExceptionFactory.conflict("User {data.email} already exists")
    return new_user


@router.patch("/users/{user_id:int}")
def edit_user(
    db: DbSessionDep,
    request_user: AdminUserDep,
    user_id: int,
    data: UserEdit,
) -> UserRead:
    query = select(User).where(User.id == user_id)
    user = db.scalars(query).first()

    if not user:
        raise HTTPExceptionFactory.not_found("User {user}")

    update_object(
        user, data.model_dump(exclude_unset=True, exclude=["companies_ids"])
    )
    user.companies = (
        db.execute(select(Company).where(Company.id.in_(data.companies_ids)))
        .scalars()
        .all()
    )
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPExceptionFactory.conflict("User {user.email}")
    return user
