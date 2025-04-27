class Vacancy:
    __slots__ = [
        "name",
        "salary_from",
        "salary_to",
        "url",
        "requirement",
    ]  # ограничиваем атрибуты

    def __init__(
        self, name: str, salary_from: int, salary_to: int, url: str, requirement: str
    ):
        self.name = self.__validate_string(name, "Name")
        self.salary_from = self.__validate_salary(salary_from)
        self.salary_to = self.__validate_salary(salary_to)
        self.url = self.__validate_string(url, "URL")
        self.requirement = self.__validate_string(requirement, "Requirement")

    def to_dict(self):
        """Метод для преобразования объекта Vacancy в словарь."""
        return {
            "name": self.name,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "url": self.url,
            "requirement": self.requirement,
        }

    def __validate_salary(self, salary: int) -> int:
        """
        Приватный метод для проверки корректности зарплаты.
        Зарплата должна быть положительным числом или нулем.
        """
        if not salary or salary is None:
            return 0
        if salary < 0:
            raise ValueError(
                f"Зарплата должна быть положительным числом или нулем. Получено: {salary}"
            )
        return salary

    def __validate_string(self, value: str, field_name: str) -> str:
        """
        Приватный метод для проверки строковых данных.
        Проверяет, что строка не пуста.
        """
        if not value or not isinstance(value, str):
            return "Нет информации"
        return value

    def __lt__(self, other):
        """
        Сравниваем вакансии по минимальной зарплате.
        """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from < other.salary_from

    def __eq__(self, other):
        """
        Проверка на равенство вакансий по зарплате.
        """
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from == other.salary_from

    def __repr__(self):
        return (
            f"Vacancy(name={self.name}, salary_from={self.salary_from},"
            f"salary_to={self.salary_to}, url={self.url}, requirement={self.requirement})"
        )
