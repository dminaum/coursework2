from abc import ABC, abstractmethod


class Parser(ABC):
    def __init__(self, file_worker):
        self.file_worker = file_worker
        self.vacancies = []

    @abstractmethod
    def load_vacancies(self, keyword):
        """
        Загружает вакансии по ключевому слову.
        """
        pass

    def get_vacancies(self):
        """
        Возвращает загруженные вакансии.
        """
        return self.vacancies

    def save_to_file(self):
        """
        Сохраняет вакансии в файл через file_worker
        """
        self.file_worker.write(self.vacancies)


