from unittest.mock import MagicMock, patch

import pytest

from src.parsers.hh_api import HeadHunterAPI


@pytest.fixture
def fake_file_worker():
    """Фикстура для поддельного file_worker"""

    class FakeFileWorker:
        def save(self, data):
            self.data = data

    return FakeFileWorker()


@pytest.fixture
def hh_api(fake_file_worker):
    """Фикстура для экземпляра HeadHunterAPI"""
    return HeadHunterAPI(fake_file_worker)


@patch("src.parsers.hh_api.requests.get")
def test_load_vacancies(mock_get, hh_api):
    """Тест загрузки вакансий с API"""

    # Подготавливаем фейковые ответы API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "pages": 2,
        "items": [
            {"id": "1", "name": "Python Developer"},
            {"id": "2", "name": "Backend Developer"},
        ],
    }
    mock_get.return_value = mock_response

    # Вызываем метод
    vacancies = hh_api.load_vacancies("Python")

    # Проверки
    assert isinstance(vacancies, list)
    assert len(vacancies) > 0
    assert vacancies[0]["name"] == "Python Developer"
    assert hasattr(hh_api.json_saver, "data")
    assert hh_api.json_saver.data == vacancies


@patch("src.parsers.hh_api.requests.get")
def test_connect_failure(mock_get, hh_api):
    """Тест ошибки подключения к API"""

    # Подготавливаем ответ с ошибкой
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    # Проверяем, что выбрасывается исключение
    with pytest.raises(Exception) as excinfo:
        hh_api._HeadHunterAPI__connect()

    assert "Ошибка подключения" in str(excinfo.value)
