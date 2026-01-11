import psycopg2


class DBManager:
    """подключается к БД PostgreSQL и имеет методы по работе с БД"""

    def __init__(self, param):
        self.param = param
        self.conn = psycopg2.connect(**param)


    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """ получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        pass
