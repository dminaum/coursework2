import pytest
from src.utils.helpers import (
    remove_html_tags,
    from_api_to_list,
    filter_vacancies_by_salary,
    get_top_vacancies,
    filter_vacancies_by_keyword,
)

from src.vacancies.vacancy import Vacancy


@pytest.fixture
def sample_api_vacancies():
    return [
        {
            'name': 'Python Developer',
            'salary': {'from': 100000, 'to': 150000},
            'alternate_url': 'http://example.com/vacancy/1',
            'snippet': {'requirement': '<b>Python</b> skills required'}
        },
        {
            'name': 'Backend Developer',
            'salary': None,
            'alternate_url': 'http://example.com/vacancy/2',
            'snippet': {'requirement': 'Experience with Django'}
        }
    ]


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy('Python Developer', 100000, 150000, 'http://example.com/vacancy/1', 'Python skills required'),
        Vacancy('Backend Developer', 0, 0, 'http://example.com/vacancy/2', 'Experience with Django'),
        Vacancy('Junior Developer', 50000, 70000, 'http://example.com/vacancy/3', 'HTML, CSS knowledge'),
    ]


def test_remove_html_tags():
    html_text = "<b>Hello</b> <i>World</i>"
    clean_text = remove_html_tags(html_text)
    assert clean_text == "Hello World"


def test_from_api_to_list(sample_api_vacancies):
    vacancies = from_api_to_list(sample_api_vacancies)
    assert len(vacancies) == 2
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].name == "Python Developer"
    assert vacancies[1].salary_from == 0
    assert vacancies[1].salary_to == 0


def test_filter_vacancies_by_salary(sample_vacancies):
    filtered = filter_vacancies_by_salary(sample_vacancies, 90000, 160000)
    assert len(filtered) == 1
    assert filtered[0].name == "Python Developer"

    filtered_empty = filter_vacancies_by_salary(sample_vacancies, 200000, 300000)
    assert len(filtered_empty) == 0


def test_get_top_vacancies(sample_vacancies):
    top_vacancies = get_top_vacancies(sample_vacancies, 2)
    assert len(top_vacancies) == 2
    assert top_vacancies[0].salary_from >= top_vacancies[1].salary_from


def test_filter_vacancies_by_keyword(sample_vacancies):
    filtered = filter_vacancies_by_keyword(sample_vacancies, ['Python', 'HTML'])
    assert len(filtered) == 2
    names = [vacancy.name for vacancy in filtered]
    assert "Python Developer" in names
    assert "Junior Developer" in names

    no_match = filter_vacancies_by_keyword(sample_vacancies, ['C++'])
    assert len(no_match) == 0
