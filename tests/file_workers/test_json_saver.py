import json
import os
import sys
import pytest
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.file_workers.json_saver import JSONSaver

# Создаём временный путь для тестового файла
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
    return {
        "id": "1",
        "name": "Python Developer",
        "area": {"name": "Москва"},
        "salary_from": 100000,
        "salary_to": 150000,
        "url": "https://example.com/vacancy/1",
        "requirement": "Опыт работы от 3 лет",
        "responsibility": "Разработка и поддержка"
    }


def test_save_and_read(json_saver, sample_vacancy):
    """Тест на сохранение и чтение данных"""
    json_saver.save([sample_vacancy])
    data = json_saver.read()
    assert isinstance(data, list)
    assert data[0]['name'] == "Python Developer"


def test_add_vacancy(json_saver, sample_vacancy):
    """Тест на добавление вакансии"""
    json_saver.save([])
    json_saver.add_vacancy(sample_vacancy)
    data = json_saver.read()
    assert sample_vacancy in data


def test_delete_vacancy(json_saver, sample_vacancy):
    """Тест на удаление вакансии"""
    json_saver.save([sample_vacancy])
    json_saver.delete_vacancy(sample_vacancy)
    data = json_saver.read()
    assert sample_vacancy not in data


def test_read_nonexistent_file():
    """Тест на чтение несуществующего файла"""
    non_existent_path = Path(__file__).parent / "nonexistent.json"
    saver = JSONSaver(path_to_file=non_existent_path)
    assert saver.read() == []
