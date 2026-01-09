from abc import ABC, abstractmethod

import requests
from requests import Response


class VacanciesAPI(ABC):
    """Абстрактный класс для работы с API сервиса вакансий."""

    @abstractmethod
    def _api_connections(self):
        """Метод проверки API происходит проверка статус-кода ответа."""
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str, region: str, days: int):
        """Метод получения данных API сервиса вакансий."""
        pass


class HH(VacanciesAPI):
    """Класс для работы с API сервиса вакансий с платформой hh.ru."""

    def __init__(self) -> None:
        """url - адрес API,
        headers - заголовок
        params - параметры запроса
            (text - Переданное значение ищется в полях вакансии
            page - Номер страницы
            per_page - Количество элементов
            search_field - Область поиска text
            area - Регион. Необходимо передавать id из справочника /areas. Можно указать несколько значений
            period - Количество дней, в пределах которых производится поиск по вакансиям)"""

        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 5, "search_field": "name", "area": "", "period": ""}
        self.__vacancies = []

    def _api_connections(self) -> Response | None:
        """Метод проверки API. Происходит проверка статус-кода ответа hh.ru."""

        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            response.raise_for_status()
            return response
        except Exception as e:
            print(e)

    def load_vacancies(self, keyword: str, region="113", days=7) -> list:
        """Метод получения данных API сервиса вакансий с платформой hh.ru."""

        self.__params["text"] = keyword
        self.__params["area"] = region
        self.__params["period"] = days

        while self.__params.get("page") != 5:
            response = self._api_connections()
            vacancies = response.json()["items"]
            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1
        return self.__vacancies
