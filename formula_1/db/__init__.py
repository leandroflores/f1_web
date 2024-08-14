from formula_1.config import settings
from logging import Logger

from sqlalchemy import (
    create_engine,
    MetaData,
    select,
    true,
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


def create_admin_user(logger: Logger):
    from formula_1.db.models import Company, Organization, User

    query_admin = select(User).where(
        User.is_admin == true() and User.email == "admin@f1race.com"
    )
    with SessionLocal() as db_session:
        user = db_session.scalars(query_admin).first()
        if not user:
            logger.info("**** No admin user found ****")
            logger.info("**** Creating admin user... ****")
            organization = Organization(name="Grupo LF")
            company = Company(name="F1 Race", organization=organization)
            db_session.add(organization)
            db_session.add(company)
            db_session.add(
                User(
                    email="admin@f1race.com",
                    is_admin=True,
                    is_active=True,
                    is_master=True,
                    password="123",
                    full_name="Admin F1 Race",
                    organization=organization,
                    companies=[company],
                )
            )
            db_session.commit()
