import json
from pathlib import Path

from src.file_workers.base import Saver
from src.vacancies.vacancy import Vacancy

MAIN_DIR = Path(__file__).resolve().parent.parent.parent
PATH_TO_JSON = MAIN_DIR / "data" / "vacancies1.json"


class JSONSaver(Saver):
    def __init__(self, path_to_file=PATH_TO_JSON):
        super().__init__(path_to_file)

    def save(self, data: list):
        with open(self.path_to_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def read(self) -> list[dict]:
        try:
            with open(self.path_to_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_vacancy(self, vacancy: Vacancy):
        try:
            current_data = self.read()
        except (FileNotFoundError, json.JSONDecodeError):
            current_data = []

        if vacancy not in current_data:
            current_data.append(vacancy.to_dict())
            self.save(current_data)

    def delete_vacancy(self, vacancy: Vacancy):
        try:
            data = self.read()
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        if vacancy in data:
            data.remove(vacancy.to_dict())
            self.save(data)
