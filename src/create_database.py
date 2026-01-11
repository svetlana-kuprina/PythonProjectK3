from typing import Any

import psycopg2

from src.config import config


def database_exists(cursor, db_name):
    """Функция для проверки базы данных"""

    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
    return cursor.fetchone() is not None



def create_database(database_name: str, params: dict):
    """Функция для создания базы данных, если она не существует"""

    try:
        conn = psycopg2.connect(database="postgres", **params, connect_timeout=5)
        conn.autocommit = True
        with conn.cursor() as cur:
            if not database_exists(cur, database_name):
                cur.execute(f"CREATE DATABASE {database_name}")
            else:
                print(f"База данных {database_name} уже существует.")

    except psycopg2.Error as e:
        print(f"Ошибка при проверке базы данных: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def create_tables_employers(database_name: str, params: dict):
    """Функция для создания таблиц в базе данных, если они не существуют"""

    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        try:
            cur.execute("""CREATE TABLE employers (
            employers_id SERIAL PRIMARY KEY,
            name_employers VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            description VARCHAR(255)) """)
        except psycopg2.errors.DuplicateTable:
            print('Таблица "employers" уже существует')
        conn.commit()
        conn.close()

def create_tables_vacancies(database_name: str, params: dict):
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        try:
            cur.execute("""CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            employers_id int NOT NULL,
            FOREIGN KEY (employers_id) REFERENCES employers (employers_id) ON DELETE CASCADE,
            name_vacancies VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            experience VARCHAR(100),
            schedule VARCHAR(100),
            salary VARCHAR(100),
            description VARCHAR(255))""")
        except psycopg2.errors.DuplicateTable:
            print('Таблица "vacancies" уже существует')
        conn.commit()
        conn.close()


def save_to_db_employers(data: list[str:Any], params: dict, database_name) -> None:
    """Сохранение данных об организациях в базу данных"""

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for data_dict in data:
            name = data_dict.get('name')
            url = data_dict.get('url')
            experience = data_dict.get('experience')
            schedule = data_dict.get('schedule')
            salary = data_dict.get('salary')
            description = data_dict.get('description')
            cur.execute(
                """
                INSERT INTO channels (name, url, experience, schedule, salary, description)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING channel_id
                """,
                (name, url, experience, schedule, salary, description))

        conn.commit()
        conn.close()

def save_to_db_vacancies(data: list[str:Any], params: dict, database_name) -> None:
    """Сохранение данных о вакансиях в базу данных"""

    pass

def main_m():
    # получаем параметры базы данных
    params = config()
    database_name = 'hh'
    # создаем базу и таблицы
    create_database(database_name, params)
    create_tables_employers(database_name, params)
    create_tables_vacancies(database_name, params)

if __name__ == '__main__':
    main_m()
