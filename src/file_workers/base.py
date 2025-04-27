from abc import ABC, abstractmethod


class Saver(ABC):
    def __init__(self, path_to_file):
        try:
            self.__path_to_file = path_to_file
        except OSError:
            print("Файл не найден.")

    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass

    @property
    def path_to_file(self):
        return self.__path_to_file

    @path_to_file.getter
    def path_to_file(self):
        return self.__path_to_file
