import os
import sys
from pathlib import Path

import pytest

from src.file_workers.json_saver import JSONSaver
from src.vacancies.vacancy import Vacancy  # Импортируем класс Vacancy

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

TEST_FILE_PATH = Path(__file__).parent / "test_vacancies.json"


@pytest.fixture
def json_saver():
    """Фикстура для работы с JSONSaver"""
    saver = JSONSaver(path_to_file=TEST_FILE_PATH)
    yield saver
    if TEST_FILE_PATH.exists():
        os.remove(TEST_FILE_PATH)


@pytest.fixture
def sample_vacancy():
    """Фикстура для создания тестовой вакансии"""
    return Vacancy(
        name="Python Developer",
        salary_from=100000,
        salary_to=150000,
        url="https://example.com/vacancy/1",
        requirement="Опыт работы от 3 лет",
    )


def test_save_and_read(json_saver, sample_vacancy):
    """Тест на сохранение и чтение данных"""
    json_saver.save([sample_vacancy.to_dict()])  # Сохраняем вакансию как словарь
    data = json_saver.read()
    assert isinstance(data, list)
    assert data[0]["name"] == "Python Developer"


def test_add_vacancy(json_saver, sample_vacancy):
    """Тест на добавление вакансии"""
    json_saver.save([])  # Сохраняем пустой список
    json_saver.add_vacancy(sample_vacancy)  # Добавляем вакансию как объект
    data = json_saver.read()  # Читаем данные из файла
    assert sample_vacancy.to_dict() in data  # Проверяем, что вакансия добавлена


def test_delete_vacancy(json_saver, sample_vacancy):
    """Тест на удаление вакансии"""
    json_saver.save([sample_vacancy.to_dict()])  # Сохраняем вакансию как словарь
    json_saver.delete_vacancy(sample_vacancy)  # Удаляем вакансию как объект
    data = json_saver.read()  # Читаем данные из файла
    assert sample_vacancy not in data  # Проверяем, что вакансия удалена


def test_read_nonexistent_file():
    """Тест на чтение несуществующего файла"""
    non_existent_path = Path(__file__).parent / "nonexistent.json"
    saver = JSONSaver(path_to_file=non_existent_path)
    assert saver.read() == []  # Ожидаем пустой список при чтении несуществующего файла
