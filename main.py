from src.API_vacancies import HH
from src.DBManager_vacancies import DBManager
from src.config import config
from src.create_database import create_database, save_to_db_employers, create_tables_vacancies, create_tables_employers


def main():
    # получаем параметры базы данных
    params = config()
    database_name = 'hh'
    # создаем базу и таблицы
    create_database(database_name, params)
    create_tables_employers(database_name, params)
    create_tables_vacancies(database_name, params)

    list_employer_id = ['2180','2748','3529','8884','1959252','68587','1740','3192913','9498112','2523']
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_employers_list = []
    hh_vacancies_list = []

    for employer_id in list_employer_id:
        api = HH(employer_id=employer_id)
        # Получение вакансий с hh.ru в формате JSON
        hh_employers = api.api_connections_employers()
        hh_vacancies = api.api_connections_vacancies()
        hh_employers_list.append(hh_employers)
        hh_vacancies_list.append(hh_vacancies)

    # сохраняем полученные из API данные в базу данных
    save_to_db_employers(hh_employers_list,hh_vacancies_list, params, database_name)

    #Вывод информации по вакансиям из БД
    db_men = DBManager(database_name, params)
    print(""" 
    
    Вывод информации с сайта hh.ru по вакансиям id организаций:
     (2180','2748','3529','8884','1959252','68587','1740','3192913','9498112','2523)
      
      """)
    print("____________список всех компаний и количество вакансий у каждой компании________________")
    print(db_men.get_companies_and_vacancies_count())
    print('''
    ___список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию___
    ''')
    print(db_men.get_all_vacancies())
    print('''
    _______________________________средняя зарплата по вакансиям_____________________________
    ''')
    print(db_men.get_avg_salary())
    print('''
    ____________список всех вакансий, у которых зарплата выше средней по всем вакансиям________________
    ''')
    print(db_men.get_vacancies_with_higher_salary())
    print('''
    ____ список всех вакансий, в названии которых содержатся слова, например python___
    ''')
    keyword = input('Введите значение поиска: ')
    print(db_men.get_vacancies_with_keyword(keyword))





if __name__ == '__main__':
    main()