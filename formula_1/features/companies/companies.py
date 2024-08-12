import logging

from datetime import datetime
from fastapi import APIRouter
from formula_1.auth.dependencies import ActiveUserDep, AdminUserDep
from formula_1.db import SessionLocal
from formula_1.db.dependencies import DbSessionDep
from formula_1.db.models import Company, Organization
from formula_1.features.errors import HTTPExceptionFactory
from formula_1.utils import update_object
from psycopg import IntegrityError
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

router = APIRouter()
logger = logging.getLogger(__name__)


class OrganizationRead(BaseModel):
    id: int
    name: str


class CompanyRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    is_active: bool
    organization: OrganizationRead | None


class CompanyCreate(BaseModel):
    name: str
    is_active: bool = True
    organization_id: int | None


class CompanyEdit(BaseModel):
    name: str
    is_active: bool = True
    organization_id: int | None


@router.get("/companies")
def list_companies(
    request_user: ActiveUserDep,
) -> list[CompanyRead]:
    if request_user.is_master:
        query = (
            select(Company)
            .options(joinedload(Company.organization))
            .order_by(Company.name.asc())
        )
    elif request_user.is_admin:
        query = (
            select(Company)
            .options(joinedload(Company.organization))
            .where(Company.organization_id == request_user.organization_id)
            .order_by(Company.name.asc())
        )
    else:
        companies_ids: list[int] = [
            company["id"] for company in request_user.companies_ids
        ]
        query = (
            select(Company)
            .options(joinedload(Company.organization))
            .where(Company.id.in_(companies_ids))
            .order_by(Company.name.asc())
        )
    with SessionLocal() as db_session:
        companies = db_session.scalars(query).all()
    return companies


@router.post("/companies")
def create_company(
    db: DbSessionDep, request_user: AdminUserDep, data: CompanyCreate
) -> CompanyRead:
    company = Company(
        **data.model_dump(exclude=["organization_id"]),
    )

    org = db.scalars(
        select(Organization).where(Organization.id == data.organization_id)
    ).first()
    company.organization = org

    try:
        db.add(company)
        db.commit()
        db.refresh(company)
    except IntegrityError:
        db.rollback()
        raise HTTPExceptionFactory.conflict(
            f"Company {data.name} already exists"
        )
    return company


@router.patch("/companies/{company_id:int}")
def edit_company(
    db: DbSessionDep,
    request_user: AdminUserDep,
    company_id: int,
    data: CompanyEdit,
) -> CompanyRead:
    query = select(Company).where(Company.id == company_id)
    company = db.scalars(query).first()

    if not company:
        raise HTTPExceptionFactory.not_found("Company {company}")

    update_object(company, data.model_dump(exclude_unset=True))
    try:
        db.commit()
        db.refresh(company)
    except IntegrityError:
        db.rollback()
        raise HTTPExceptionFactory.conflict("Company {data.name}")
    return company
