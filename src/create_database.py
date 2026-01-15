from typing import Any

import psycopg2


def database_exists(cursor, db_name: str) -> bool:
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
        if "conn" in locals():
            conn.close()


def create_tables_employers(database_name: str, params: dict) -> None:
    """Функция для создания таблиц в базе данных, если они не существуют"""

    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        try:
            cur.execute(
                """CREATE TABLE employers
                           (
                               employers_id   SERIAL PRIMARY KEY,
                               name_employers VARCHAR(255) NOT NULL,
                               url            VARCHAR(255) NOT NULL,
                               description    TEXT
                           ) """
            )
        except psycopg2.errors.DuplicateTable:
            print('Таблица "employers" уже существует')
        except psycopg2.errors.UniqueViolation as e:
            print(e)
            conn.close()


def create_tables_vacancies(database_name: str, params: dict) -> None:
    """Функция для создания таблиц в базе данных, если они не существуют"""

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        try:
            cur.execute(
                """CREATE TABLE vacancies
                           (
                               id             SERIAL PRIMARY KEY,
                               employers_id   int          NOT NULL,
                               FOREIGN KEY (employers_id) REFERENCES employers (employers_id) ON DELETE CASCADE,
                               name_vacancies VARCHAR(255) NOT NULL,
                               url            VARCHAR(255) NOT NULL,
                               experience     VARCHAR(100),
                               schedule       VARCHAR(100),
                               salary_from    INT,
                               salary_to      INT,
                               description    TEXT
                           )"""
            )
        except psycopg2.errors.DuplicateTable:
            print('Таблица "vacancies" уже существует')
        conn.commit()
        conn.close()


def save_to_db_employers(data: list[str:Any], data_vac: list[str:Any], params: dict, database_name) -> None:
    """Сохранение данных в базу данных"""

    try:
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            for data_dict in data:
                name = data_dict.get("name")
                url = data_dict.get("alternate_url")
                description = data_dict.get("description")
                cur.execute(
                    """
                    INSERT INTO employers (name_employers, url, description)
                    VALUES (%s, %s, %s) RETURNING employers_id
                    """,
                    (name, url, description),
                )
                employers_id = cur.fetchone()[0]

                for data_dict_list in data_vac:
                    for data_dict_vac in data_dict_list:
                        name = data_dict_vac.get("name")
                        url = data_dict_vac.get("alternate_url")
                        experience = data_dict_vac.get("description")
                        schedule = data_dict_vac.get("schedule")
                        salary = data_dict_vac.get("salary")
                        if salary == None:
                            salary = {"from": None, "to": None}
                        description = data_dict_vac.get("description")
                        cur.execute(
                            """
                            INSERT INTO vacancies (employers_id, name_vacancies, url, experience, schedule, salary_from,
                                                   salary_to, description)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """,
                            (
                                employers_id,
                                name,
                                url,
                                experience,
                                schedule["name"],
                                salary.get("from"),
                                salary.get("to"),
                                description,
                            ),
                        )
            conn.commit()
            conn.close()
    except psycopg2.Error as e:
        print(e)
