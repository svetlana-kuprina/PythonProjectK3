from src.API_vacancies import HH
from src.config import config
from src.create_database import create_database, save_data_to_db

def main():


    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HH()

    # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = hh_api.load_vacancies("Программист", "3", 10)
    # for vacancy in hh_vacancies:
    #     print(vacancy)

    # получаем параметры базы данных
    params = config()
    # создаем базу и таблицы
    create_database(params)
    # сохраняем полученные из API данные в базу данных
    save_data_to_db(hh_vacancies, params)


if __name__ == '__main__':
    main()