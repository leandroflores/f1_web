import json
import os
import requests

URL_BASE: str = "http://ergast.com/api/f1"
DATA_PATH: str = "data"

def _create_file(year: int, entity: str) -> bool:
    try:
        url: str = f"{URL_BASE}/{year}/{entity}s.json"
        path: str = f"{DATA_PATH}/{year}/{entity}s_" + str(year) + ".json"
        response: requests.Response = requests.get(url)
        data: str = json.dumps(response.json())
        if not os.path.isfile(path):
            with open(path, "w") as file:
                file.write(data)
        return True
    except Exception:
        return False


def create_races_files(year: int, rounds: int) -> bool:
    for round in range(1, rounds + 1):
        create_race_file(year, round)

def create_season_file(year: int) -> bool:
    try:
        folder_path: str = f"data/{year}"
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

            url: str = f"{URL_BASE}/{year}.json"
            path: str = f"{DATA_PATH}/{year}/{year}.json"
            response: requests.Response = requests.get(url)
            data: str = response.json()
            total: int = int(data["MRData"]["total"])
            if not os.path.isfile(path):
               with open(path, "w") as file:
                    file.write(json.dumps(data))

            create_races_files(year, total)
            create_circuit_file(year)
            create_driver_file(year)
            create_constructor_file(year)
            
        return True
    except Exception:
        return False
    
def create_race_file(year: int, round: int) -> bool:
    try:
        url: str = f"{URL_BASE}/{year}/{round}/results.json"
        path: str = f"{DATA_PATH}/{year}/{year}_{round}.json"
        response: requests.Response = requests.get(url)
        data: str = json.dumps(response.json())
        if not os.path.isfile(path):
            with open(path, "w") as file:
                file.write(data)
        return True
    except Exception:
        return False

def create_circuit_file(year: int) -> bool:
    _create_file(year, "circuit")

def create_driver_file(year: int) -> bool:
    _create_file(year, "driver")

def create_constructor_file(year: int) -> bool:
    _create_file(year, "constructor")
    

years: list[int] = [2008]
for year in years:
    print(year)
    print(create_season_file(year))