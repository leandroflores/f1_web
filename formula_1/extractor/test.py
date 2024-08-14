import json
import os

from formula_1.db import SessionLocal
from formula_1.db.models import Constructor, Driver

from sqlalchemy import select, true

DATA_PATH: str = "data"

def import_constructors(year: int) -> bool:
    response: dict = {}
    file_path: str = f"{DATA_PATH}/{year}/constructors_{year}.json"
    print(file_path)
    if os.path.isfile(file_path):
        print("Teste")
        with open(file_path, "r") as file:
            response: dict = json.loads(file.read())
    
    print("0" * 50)
    print(response)
    print("0" * 50)

    response_data: dict = response["MRData"]
    for data in response_data["ConstructorTable"]["Constructors"]:
        query_constructor = select(Constructor).where(
            Constructor.identifier == data["constructorId"]
        )
        with SessionLocal() as session_db:
            constructor = session_db.scalars(query_constructor).first()
            if constructor:
                 continue

            new_constructor: Constructor = Constructor()
            new_constructor.identifier = data["constructorId"]
            new_constructor.name = data["name"]
            new_constructor.nationality = data["nationality"]
            new_constructor.url = data["url"]
            print(new_constructor)
            session_db.add(new_constructor)
            session_db.commit()

def import_drivers(year: int) -> dict:
    try:
        response: dict = {}
        file_path: str = f"{DATA_PATH}/{year}/drivers_{year}.json"
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                response: dict = json.loads(file.read())
        driver_data: dict = response["MRData"]
        for data in driver_data["DriverTable"]["Drivers"]:
            query_driver = select(Driver).where(
                Driver.identifier == data["driverId"]
            )
            with SessionLocal() as session_db:
                try:
                    driver = session_db.scalars(query_driver).first()
                    if driver:
                        continue

                    new_driver: Driver = Driver.from_dict(data)
                    session_db.add(new_driver)
                    session_db.commit()
                except Exception :
                    session_db.rollback()

    except Exception as e:
        import traceback
        traceback.print_exc(e)
        return {}

years: list[int] = [2012]
for year in years:
    import_constructors(year)
    import_drivers(year)