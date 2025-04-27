import requests

from src.parsers.base import Parser


class HeadHunterAPI(Parser):
    """
       Класс для работы с API HeadHunter
       """

    def __init__(self, file_worker):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.json_saver = file_worker
        super().__init__(file_worker)

    def __connect(self):
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        if response.status_code != 200:
            raise Exception(f"Ошибка подключения: {response.status_code}")
        return response.json()

    def load_vacancies(self, keyword):
        self.__params['text'] = keyword
        response = self.__connect()
        total_pages = response['pages']

        all_vacancies = []

        for page in range(total_pages):
            self.__params['page'] = page
            response = self.__connect()
            vacancies = response.get('items', [])
            all_vacancies.extend(vacancies)  # Добавляем вакансии в список

        self.json_saver.save(all_vacancies)  # Сохраняем все вакансии в файл
        return all_vacancies