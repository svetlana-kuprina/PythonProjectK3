import psycopg2


class DBManager:
    """подключается к БД PostgreSQL и имеет методы по работе с БД"""

    def __init__(self, database_name: str, params) -> None:
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех компаний и количество вакансий у каждой компании."""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """SELECT name_employers, COUNT(vacancies.name_vacancies)
                               FROM employers
                                        JOIN vacancies USING (employers_id)
                               GROUP BY employers.name_employers"""
                )

            except psycopg2.Error as e:
                print(e)
            return cur.fetchall()

    def get_all_vacancies(self):
        """Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """SELECT employers.name_employers, name_vacancies, salary_from, salary_to, vacancies.url
                               FROM vacancies
                                        JOIN employers USING (employers_id)"""
                )

            except psycopg2.Error as e:
                print(e)
            return cur.fetchall()

    def get_avg_salary(self):
        """Метод получает среднюю зарплату по вакансиям"""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            try:
                cur.execute("""SELECT AVG(salary_from), AVG (salary_to) FROM vacancies""")

            except psycopg2.Error as e:
                print(e)
            return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """SELECT *
                               FROM vacancies
                               WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
                                  OR salary_to > (SELECT AVG(salary_to) FROM vacancies)"""
                )

            except psycopg2.Error as e:
                print(e)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Метод получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python"""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            try:
                cur.execute(f"""SELECT * FROM vacancies WHERE name_vacancies LIKE '%{keyword}%';""")

            except psycopg2.Error as e:
                print(e)
            return cur.fetchall()
