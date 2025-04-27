from src.file_workers.json_saver import JSONSaver
from src.parsers.hh_api import HeadHunterAPI
from src.utils.helpers import (
    filter_vacancies_by_keyword,
    filter_vacancies_by_salary,
    from_api_to_list,
    get_top_vacancies,
    print_vacancies,
)


# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    key_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    while True:
        salary_range = input("Введите диапазон зарплат (например, 100000 - 150000): ")
        try:
            salary_from, salary_to = map(int, salary_range.split(" - "))
            break  # Выход из цикла, если формат правильный
        except ValueError:
            print("Неверный формат диапазона зарплат. Попробуйте снова.")

    file_worker = JSONSaver("data/vacancies1.json")
    vacancies_result = JSONSaver("data/result_vacancies.json")
    hh_api = HeadHunterAPI(file_worker)

    response_list = hh_api.load_vacancies(search_query)

    vacancies_list = from_api_to_list(response_list)

    # Фильтруем вакансии по ключевым словам
    filtered_vacancies = filter_vacancies_by_keyword(vacancies_list, key_words)

    # Фильтруем по диапазону зарплат
    ranged_vacancies = filter_vacancies_by_salary(
        filtered_vacancies, salary_from, salary_to
    )

    # Получаем топ-N вакансий
    top_vacancies = get_top_vacancies(ranged_vacancies, top_n)

    vacancies_dict_list = [vacancy.to_dict() for vacancy in top_vacancies]
    vacancies_result.save(vacancies_dict_list)
    # Печатаем вакансии
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
