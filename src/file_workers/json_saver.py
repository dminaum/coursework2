import json
from pathlib import Path

from src.file_workers.base import Saver
from src.vacancies.vacancy import Vacancy

MAIN_DIR = Path(__file__).resolve().parent.parent.parent
PATH_TO_JSON = MAIN_DIR / "data" / "vacancies1.json"


class JSONSaver(Saver):
    def __init__(self, path_to_file: Path = PATH_TO_JSON):
        self.__path_to_file = path_to_file

    @property
    def path_to_file(self):
        return self.__path_to_file

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
        data = self.read()
        if vacancy.to_dict() not in data:
            data.append(vacancy.to_dict())
            self.save(data)

    def delete_vacancy(self, vacancy: Vacancy):
        data = self.read()
        if vacancy.to_dict() in data:
            data.remove(vacancy.to_dict())
            self.save(data)
