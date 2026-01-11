from src.API_vacancies import HH
from src.config import config
from src.create_database import create_database, save_to_db_employers, create_tables_vacancies, create_tables_employers, \
    save_to_db_vacancies


def main():
    # получаем параметры базы данных
    params = config()
    database_name = 'hh'
    # создаем базу и таблицы
    create_database(database_name, params)
    create_tables_employers(database_name, params)
    create_tables_vacancies(database_name, params)


# list_employer_id = ['2180','2748','3529','8884','1959252','68587','1740','3192913','9498112','2523']
    # # Создание экземпляра класса для работы с API сайтов с вакансиями
    # for employer_id in list_employer_id:
    #     api = HH(employer_id=employer_id)
    #     # Получение вакансий с hh.ru в формате JSON
    #     hh_employers = api.api_connections_employers()
    #     hh_vacancies = api.api_connections_vacancies()
    #
    #     # сохраняем полученные из API данные в базу данных
    #     save_to_db_employers(hh_employers, params, database_name)
    #     save_to_db_vacancies(hh_vacancies, params, database_name)



if __name__ == '__main__':
    main()