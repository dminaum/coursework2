from abc import ABC, abstractmethod


class Saver(ABC):
    @property
    @abstractmethod
    def path_to_file(self):
        """Возвращает путь к файлу"""
        pass

    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass
