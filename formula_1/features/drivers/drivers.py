import logging

from datetime import date, datetime
from fastapi import APIRouter
from formula_1.auth.dependencies import ActiveUserDep, AdminUserDep
from formula_1.db import SessionLocal
from formula_1.db.dependencies import DbSessionDep
from formula_1.db.models import Driver
from formula_1.features.errors import HTTPExceptionFactory
from formula_1.utils import update_object
from psycopg import IntegrityError
from pydantic import BaseModel
from sqlalchemy import select

router = APIRouter()
logger = logging.getLogger(__name__)


class DriverRead(BaseModel):
    id: int
    identifier: str
    code: str
    first_name: str
    last_name: str
    birth_date: date | None
    country: str
    url: str

class DriverCreate(BaseModel):
    id: int
    identifier: str
    code: str
    first_name: str
    last_name: str
    birth_date: date | None
    country: str
    url: str

class DriverEdit(BaseModel):
    id: int
    identifier: str
    code: str
    first_name: str
    last_name: str
    birth_date: date | None
    country: str
    url: str


@router.get("/drivers")
def list_drivers(
    request_user: ActiveUserDep,
) -> list[DriverEdit]:
    
    query = (
        select(Driver)
        .order_by(Driver.first_name.asc())
    )
    with SessionLocal() as db_session:
        drivers = db_session.scalars(query).all()
    return drivers


@router.post("/drivers")
def create_driver(
    db: DbSessionDep, 
    request_user: AdminUserDep, 
    data: DriverCreate
) -> DriverRead:
    driver = Driver(
        **data.model_dump(),
    )

    try:
        db.add(driver)
        db.commit()
        db.refresh(driver)
    except IntegrityError:
        db.rollback()
        raise HTTPExceptionFactory.conflict(
            f"Driver {data.code} already exists"
        )
    return driver


@router.patch("/drivers/{driver_id:int}")
def edit_driver(
    db: DbSessionDep,
    request_user: AdminUserDep,
    driver_id: int,
    data: DriverEdit,
) -> DriverRead:
    query = select(Driver).where(Driver.id == driver_id)
    driver: Driver = db.scalars(query).first()

    if not request_user.is_master:
        raise HTTPExceptionFactory.credentials()

    if not driver:
        raise HTTPExceptionFactory.not_found("Driver {driver}")

    update_object(driver, data.model_dump(exclude_unset=True))
    try:
        db.commit()
        db.refresh(driver)
    except IntegrityError:
        db.rollback()
        raise HTTPExceptionFactory.conflict("Driver {data.code}")
    return driver
