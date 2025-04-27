from src.vacancies.vacancy import Vacancy
import re


def remove_html_tags(text):
    return re.sub(r'<.*?>', '', text)


def from_api_to_list(api_vacancies):
    """
    Преобразует список вакансий из API в список объектов Vacancy.
    :param api_vacancies: Список вакансий из API.
    :return: Список объектов Vacancy.
    """
    vacancy_list = []

    for api_vacancy in api_vacancies:
        # Проверка на None и на пустоту значения 'salary'
        salary_from = 0
        salary_to = 0
        if api_vacancy.get('salary') is not None:
            salary_from = api_vacancy.get('salary', {}).get('from', 0)
            salary_to = api_vacancy.get('salary', {}).get('to', 0)

        url = api_vacancy.get('alternate_url', '')
        requirement = api_vacancy.get('snippet', {}).get('requirement', 'Нет информации')

        # Создаем объект Vacancy
        vacancy = Vacancy(
            name=api_vacancy.get('name', ''),
            salary_from=salary_from,
            salary_to=salary_to,
            url=url,
            requirement=requirement
        )
        vacancy_list.append(vacancy)

    return vacancy_list


def filter_vacancies_by_salary(vacancies: list[Vacancy], salary_from, salary_to) -> list[Vacancy]:
    """
        Фильтрует список вакансий по диапазону зарплат.

        Аргументы:
            vacancies (list[Vacancy]): Список объектов вакансий для фильтрации.
            salary_from (int): Минимальная зарплата, от которой фильтруются вакансии.
            salary_to (int): Максимальная зарплата, до которой фильтруются вакансии.

        Возвращает:
            list[Vacancy]: Список вакансий, у которых зарплата "от" больше или равна `salary_from`,
                           а зарплата "до" меньше или равна `salary_to`.
        """
    result = []
    for vacancy in vacancies:
        if salary_from <= vacancy.salary_from <= salary_to and (
                salary_from <= vacancy.salary_to <= salary_to or vacancy.salary_to == 0):
            result.append(vacancy)
    return result


def get_top_vacancies(vacancies, top_n):
    """
    Возвращает топ N вакансий по зарплате.
    :param vacancies: Список вакансий.
    :param top_n: Количество вакансий для вывода.
    :return: Топ вакансий.
    """
    sorted_vacancies = sorted(vacancies, key=lambda vacancy: vacancy.salary_from, reverse=True)
    return sorted_vacancies[:top_n]


def filter_vacancies_by_keyword(vacancies, keywords):
    """
    Фильтрует вакансии по списку ключевых слов.
    :param vacancies: Список вакансий.
    :param keywords: Список ключевых слов.
    :return: Отфильтрованные вакансии.
    """
    return [vacancy for vacancy in vacancies if
            any(keyword.lower() in vacancy.requirement.lower() for keyword in keywords)]


def print_vacancies(vacancies):
    """
    Выводит вакансии в человекочитаемом виде.
    :param vacancies: Список объектов Vacancy.
    """
    if not vacancies:
        print("Нет доступных вакансий.")
        return
    for vacancy in vacancies:
        print(f"Название: {vacancy.name}")
        if vacancy.salary_to == 0:
            print(f"Зарплата: {vacancy.salary_from}")
        else:
            print(f"Зарплата: {vacancy.salary_from} - {vacancy.salary_to}")
        print(f"Требования: {remove_html_tags(vacancy.requirement)}")
        print(f"Ссылка: {vacancy.url}")
        print('-' * 40)
