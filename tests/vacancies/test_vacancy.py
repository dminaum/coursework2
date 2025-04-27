import pytest
from src.vacancies.vacancy import Vacancy


def test_vacancy_creation_valid():
    vacancy = Vacancy("Python Developer", 100000, 150000, "http://example.com", "Experience with Django")

    assert vacancy.name == "Python Developer"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.url == "http://example.com"
    assert vacancy.requirement == "Experience with Django"


def test_vacancy_creation_with_empty_fields():
    vacancy = Vacancy("", None, None, "", None)

    assert vacancy.name == "Нет информации"
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0
    assert vacancy.url == "Нет информации"
    assert vacancy.requirement == "Нет информации"


def test_vacancy_negative_salary():
    with pytest.raises(ValueError):
        Vacancy("Python Developer", -10000, 150000, "http://example.com", "Experience with Django")


def test_to_dict_method():
    vacancy = Vacancy("Python Developer", 100000, 150000, "http://example.com", "Experience with Django")
    expected_dict = {
        'name': "Python Developer",
        'salary_from': 100000,
        'salary_to': 150000,
        'url': "http://example.com",
        'requirement': "Experience with Django"
    }
    assert vacancy.to_dict() == expected_dict


def test_vacancy_comparison_lt():
    vacancy1 = Vacancy("Junior Developer", 50000, 70000, "http://example.com/junior", "Knowledge of Python")
    vacancy2 = Vacancy("Senior Developer", 150000, 200000, "http://example.com/senior", "Advanced Python skills")

    assert vacancy1 < vacancy2
    assert not (vacancy2 < vacancy1)


def test_vacancy_comparison_eq():
    vacancy1 = Vacancy("Developer A", 80000, 100000, "http://example.com/a", "Some skills")
    vacancy2 = Vacancy("Developer B", 80000, 120000, "http://example.com/b", "Other skills")

    assert vacancy1 == vacancy2


def test_vacancy_repr():
    vacancy = Vacancy("Developer", 90000, 120000, "http://example.com", "Skills required")
    expected_repr = "Vacancy(name=Developer, salary_from=90000, salary_to=120000, url=http://example.com, requirement=Skills required)"

    assert repr(vacancy) == expected_repr
