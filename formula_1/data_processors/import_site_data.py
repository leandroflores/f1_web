import requests

from formula_1.db import SessionLocal
from formula_1.db.models import (
    Circuit, 
    Constructor, 
    Driver, 
    Race,
    RacePosition,
    Season,
)

from sqlalchemy import select
from sqlalchemy.orm.session import Session

URL_BASE: str = "http://ergast.com/api/f1"

def import_season(year: int) -> Season:
    try:
        url: str = f"{URL_BASE}/{year}.json"
        response: requests.Response = requests.get(url)
        response_data: dict = response.json()["MRData"]
        with SessionLocal() as session:
            try:
                query_season = select(Season).where(
                    Season.year == year
                )
                season: Season = session.scalars(query_season).first()
                if not season:
                    season: Season = Season()
                    season.year = year
                    season.rounds = int(response_data["total"])
                    session.add(season)
                    session.commit()

                print(f"Importing circuits from {year}...")
                import_circuits(session, year)
                print(f"Importing constructors from {year}...")
                import_constructors(session, year)
                print(f"Importing drivers from {year}...")
                import_drivers(session, year)
                
                print(f"Importing races from {year}...")
                races: list[Race] = []
                for round in range(1, season.rounds + 1):
                    print(f"Importing race {round}...")
                    races.append(
                        import_race(season, session, year, round)
                    )
                
                return season
            
            except Exception as e:
                session.rollback()
                import traceback
                traceback.print_exc(e)
                return None
    
    except Exception as e:
        import traceback
        traceback.print_exc(e)
        return None

def import_circuits(session: Session, year: int) -> list[Circuit]:
    try:
        circuits: list[Circuit] = []
        url: str = f"{URL_BASE}/{year}/circuits.json"
        response_http: requests.Response = requests.get(url)
        response: dict = response_http.json()
        response_data: dict = response["MRData"]
        for data in response_data["CircuitTable"]["Circuits"]:
            query_circuit = select(Circuit).where(
                Circuit.name == data["circuitName"]
            )
            circuit: Circuit = session.scalars(query_circuit).first()
            if circuit:
                continue

            circuit: Circuit = Circuit.from_dict(data)
            circuit.data = response
            circuits.append(circuit)
            session.add(circuit)
            session.commit()

        return circuits
    except Exception:
        return []

def import_constructors(session: Session, year: int) -> list[Constructor]:
    try:
        constructors: list[Constructor] = []
        url: str = f"{URL_BASE}/{year}/constructors.json"
        response_http: requests.Response = requests.get(url)
        response: dict = response_http.json()
        response_data: dict = response["MRData"]
        for data in response_data["ConstructorTable"]["Constructors"]:
            query_constructor = select(Constructor).where(
                Constructor.identifier == data["constructorId"]
            )
            constructor: Constructor = session.scalars(query_constructor).first()
            if constructor:
                continue

            constructor: Constructor = Constructor.from_dict(data)
            constructor.data = response
            constructors.append(constructor)
            session.add(constructor)
            session.commit()
        return constructors
    except Exception:
        return []

def import_drivers(session: Session, year: int) -> list[Driver]:
    try:
        drivers: list[Driver] = []
        url: str = f"{URL_BASE}/{year}/drivers.json"
        response_http: requests.Response = requests.get(url)
        response: dict = response_http.json()
        response_data: dict = response["MRData"]
        for data in response_data["DriverTable"]["Drivers"]:
            query_driver = select(Driver).where(
                Driver.identifier == data["driverId"]
            )
            driver: Driver = session.scalars(query_driver).first()
            if driver:
                continue

            driver: Driver = Driver.from_dict(data)
            driver.data = response
            drivers.append(driver)
            session.add(driver)
            session.commit()
    except Exception:
        return []

def import_race(
        season: Season, 
        session: Session, 
        year: int, 
        round: int,
) -> Race:
    try:
        url: str = f"{URL_BASE}/{year}/{round}/results.json"
        response_http: requests.Response = requests.get(url)
        response: dict = response_http.json()
        response_data: dict = response["MRData"]
        data: dict = response_data["RaceTable"]["Races"][0]

        race: Race = Race.from_dict(data)
        race.season_id = season.id
        query_circuit = select(Circuit).where(
            Circuit.name == data["Circuit"]["circuitName"]
        )
        race.circuit = session.scalars(query_circuit).first()
        race.data = data
        session.add(race)
        session.commit()
        
        for result_data in data["Results"]:
            import_race_position(session, result_data, race)

        return race
    except Exception:
        return None


def import_race_position(
        session: Session, 
        data: dict, 
        race: Race
) -> RacePosition:
    race_position: RacePosition = RacePosition.from_dict(data)
    race_position.data = data
    
    query_driver = select(Driver).where(
        Driver.identifier == data["Driver"]["driverId"]
    )
    driver: Driver = session.scalars(query_driver).first()
    race_position.driver = driver

    query_constructor = select(Constructor).where(
        Constructor.identifier == data["Constructor"]["constructorId"]
    )
    constructor: Constructor = session.scalars(query_constructor).first()
    race_position.constructor = constructor

    race_position.race = race

    session.add(race_position)
    session.commit()

    return race_position
    

years: list[int] = [2018]
for year in years:
    import_season(year)
    