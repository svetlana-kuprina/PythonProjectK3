import requests
from requests import Response


class HH:
    """Класс для работы с API сервиса вакансий с платформой hh.ru."""

    def __init__(self, employer_id) -> None:
        """url1 - адрес API запроса информации о работодателе,
        url2 - адрес API запроса информации о вакансиях
        employer_id - id код работодателя"""

        self.employer_id = employer_id
        self.url1 = f"https://api.hh.ru/employers/{employer_id}"
        self.url2 = f"https://api.hh.ru/vacancies?employer_id={employer_id}"


    def api_connections_employers(self) -> Response | None:
        """Метод проверки API. Происходит запрос и проверка статус-кода ответа hh.ru по работодателю."""

        try:
            response1 = requests.get(self.url1)
            response1.raise_for_status()
            employers = response1.json()
            return employers
        except requests.exceptions.HTTPError as err:
            print(err)
        except requests.exceptions.ConnectionError as err:
            print(err)
        except Exception as e:
            print(e)

    def api_connections_vacancies(self) -> Response | None:
        """Метод проверки API. Происходит запрос и проверка статус-кода ответа hh.ru по вакансиям."""

        try:
            response2 = requests.get(self.url2)
            response2.raise_for_status()
            vacancies = response2.json()["items"]
            return vacancies
        except requests.exceptions.HTTPError as err:
            print(err)
        except requests.exceptions.ConnectionError as err:
            print(err)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    api = HH(employer_id="1959252")
    print(api.api_connections_employers())
    print(api.api_connections_vacancies())