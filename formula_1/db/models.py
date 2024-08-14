from datetime import date, datetime, UTC

from formula_1.db import Base
from formula_1.db.types import HashedStr, TZDateTime
from formula_1.utils import Hash, str_to_date

from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    validates,
)
from typing import List, Optional

company_user_association = Table(
    "company_user",
    Base.metadata,
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[Hash] = mapped_column(HashedStr)
    full_name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_master: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        TZDateTime, default=datetime.now(UTC)
    )
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), index=True
    )
    created_by_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), index=True
    )

    # relationships
    created_by: Mapped[Optional["User"]] = relationship(
        back_populates="created_users", remote_side=[id]
    )
    organization: Mapped["Organization"] = relationship(
        back_populates="users",
    )
    companies: Mapped[List["Company"]] = relationship(
        back_populates="users", secondary=company_user_association
    )

    # reverses
    created_users: Mapped[List["User"]] = relationship(
        back_populates="created_by"
    )
    session: Mapped["Session"] = relationship(back_populates="user")

    @property
    def companies_ids(self) -> list[int]:
        return [{"id": c.id} for c in self.companies]

    @validates("password")
    def _validate_password(self, key, password):
        return getattr(type(self), key).type.validator(password)


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        TZDateTime, default=lambda: datetime.now(UTC)
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    # reverses
    companies: Mapped[List["Company"]] = relationship(
        back_populates="organization"
    )
    users: Mapped[List["User"]] = relationship(back_populates="organization")


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TZDateTime, default=lambda: datetime.now(UTC)
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    # relationships
    organization: Mapped[Organization] = relationship(
        back_populates="companies"
    )

    # reverses
    users: Mapped[List["User"]] = relationship(
        back_populates="companies", secondary=company_user_association
    )


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        TZDateTime, default=lambda: datetime.now(UTC)
    )
    expires_at: Mapped[datetime] = mapped_column(TZDateTime)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, unique=True
    )

    # relationships
    user: Mapped[User] = relationship(back_populates="session")


class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    rounds: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        TZDateTime, default=lambda: datetime.now(UTC)
    )

    # reverses
    races: Mapped[List["Race"]] = relationship(back_populates="season")

class Constructor(Base):
    __tablename__ = "constructors"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    name: Mapped[str]
    nationality: Mapped[str]
    url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TZDateTime, default=lambda: datetime.now(UTC)
    )

class Circuit(Base):
    __tablename__ = "circuits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    city: Mapped[str]
    country: Mapped[str]
    url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TZDateTime, default=lambda: datetime.now(UTC)
    )

    # reverses
    races: Mapped[List["Race"]] = relationship(back_populates="circuit")

class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    code: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    birth_date: Mapped[datetime]
    country: Mapped[str]
    url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TZDateTime, default=lambda: datetime.now(UTC)
    )

    @staticmethod
    def from_dict(adict: dict) -> "Driver":
        driver: Driver = Driver()
        driver.identifier = adict.get("driverId", None)
        driver.code = adict.get("code", None)
        driver.first_name = adict.get("givenName", None)
        driver.last_name = adict.get("familyName", None)
        driver.birth_date = str_to_date(adict.get("dateOfBirth", None))
        driver.country = adict.get("nationality", None)
        driver.url = adict.get("url", None)
        return driver

class Race(Base):
    __tablename__ = "races"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    round: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        TZDateTime, default=lambda: datetime.now(UTC)
    )
    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id"), index=True
    )
    circuit_id: Mapped[int] = mapped_column(
        ForeignKey("circuits.id"), index=True
    )

    # relationships
    season: Mapped[Season] = relationship(back_populates="races")
    circuit: Mapped[Circuit] = relationship(back_populates="races")