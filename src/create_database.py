from typing import Any

import psycopg2


def create_database(database_name, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS hh_vacancies (
        id SERIAL PRIMARY KEY,
        name_ VARCHAR(255) NOT NULL,
        url VARCHAR(255) NOT NULL,
        experience VARCHAR(100),
        schedule VARCHAR(100),
        salary VARCHAR(100),
        description VARCHAR(255)) """)
        conn.commit()
        conn.close()


def save_data_to_db(data: dict[str:Any], params: dict) -> None:
    """Сохранение данных о вакансиях в базу данных"""
