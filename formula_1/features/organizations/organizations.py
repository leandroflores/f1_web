import logging

from datetime import datetime
from fastapi import APIRouter
from formula_1.auth.dependencies import ActiveUserDep, AdminUserDep
from formula_1.db import SessionLocal
from formula_1.db.dependencies import DbSessionDep
from formula_1.db.models import Organization
from formula_1.features.errors import HTTPExceptionFactory
from formula_1.utils import update_object
from psycopg import IntegrityError
from pydantic import BaseModel
from sqlalchemy import select

router = APIRouter()
logger = logging.getLogger(__name__)


class CompanyRead(BaseModel):
    id: int
    name: str


class CompleteOrganizationRead(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime
    companies: list[CompanyRead] = []


class OrganizationRead(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime


class OrganizationCreate(BaseModel):
    name: str
    is_active: bool = True


class OrganizationEdit(BaseModel):
    name: str
    is_active: bool = True


@router.get("/organizations")
def list_organizations(
    request_user: ActiveUserDep,
) -> list[OrganizationRead]:
    if request_user.is_master:
        query = select(Organization).order_by(Organization.name.asc())
    else:
        query = select(Organization).where(
            Organization.id == request_user.organization_id
        ).order_by(Organization.name.asc())
    with SessionLocal() as db_session:
        organizations = db_session.scalars(query).all()
    return organizations


@router.get("/organizations/{organization_id:int}")
def get_organization(
    db: DbSessionDep,
    request_user: AdminUserDep,
    organization_id: int,
) -> CompleteOrganizationRead:
    query = select(Organization).where(Organization.id == organization_id)
    organization = db.scalars(query).first()

    if not organization:
        raise HTTPExceptionFactory.not_found("Organization {organization}")

    return organization


@router.post("/organizations")
def create_organization(
    db: DbSessionDep, request_user: AdminUserDep, data: OrganizationCreate
) -> OrganizationRead:
    new_organization = Organization(
        **data.model_dump(exclude=["organization_id"]),
    )

    print("0" * 50)
    print("Create Organization")
    print("0" * 50)

    try:
        db.add(new_organization)
        db.commit()
        db.refresh(new_organization)
    except IntegrityError:
        db.rollback()
        raise HTTPExceptionFactory.conflict(
            f"Organization {data.name} already exists"
        )
    return new_organization


@router.patch("/organizations/{organization_id:int}")
def edit_organization(
    db: DbSessionDep,
    request_user: AdminUserDep,
    organization_id: int,
    data: OrganizationEdit,
) -> OrganizationRead:
    query = select(Organization).where(Organization.id == organization_id)
    organization = db.scalars(query).first()

    if not organization:
        raise HTTPExceptionFactory.not_found("Organization {company}")

    update_object(organization, data.model_dump(exclude_unset=True))
    try:
        db.commit()
        db.refresh(organization)
    except IntegrityError:
        db.rollback()
        raise HTTPExceptionFactory.conflict("Organization {data.name}")
    return organization
