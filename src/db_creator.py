import psycopg

from src.company import HhCompany
from src.vacancy import HhVacancy


class DbCreator:

    def __init__(self, host, database, user, password, port, encoding, db_name):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.encoding = encoding
        self.db_name = db_name

    def create_database(self):
        """Метод удаления базы данных(для повторного запуска проекта) и создания базы данных
        """
        conn = psycopg.connect(host=self.host, dbname=self.database, user=self.user, password=self.password,
                               port=self.port, client_encoding=self.encoding)
        #conn.set_client_encoding('UTF8')
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(f"""UPDATE pg_database SET datallowconn = 'false' WHERE datname = '{self.db_name}'""")
            cursor.execute(f"""SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity
                           WHERE pg_stat_activity.datname = '{self.db_name}' AND pid <> pg_backend_pid()""")
            cursor.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
            cursor.execute(f"""CREATE DATABASE {self.db_name}
                               WITH
                               OWNER = '{self.user}'
                               ENCODING = 'UTF8'""")
        conn.close()

    def create_tables(self):
        """Метод создания столбцов баз данных
        """
        with psycopg.connect(host=self.host, dbname=self.db_name, user=self.user, password=self.password,
                             port=self.port, client_encoding=self.encoding) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE companies (
                        company_id INT PRIMARY KEY,
                        name VARCHAR(200) NOT NULL,
                        url VARCHAR(100)
                    )
                """)

            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id INT PRIMARY KEY,
                        company_id INT REFERENCES companies(company_id),
                        name VARCHAR(200) NOT NULL,
                        city VARCHAR(50),
                        url VARCHAR(100),
                        salary_from INT,
                        salary_to INT,
                        requirements TEXT
                    )
                """)
        conn.close()

    def save_data_to_db(self, vacancies: list[HhVacancy], companies: [HhCompany]):
        """Метод записи и сохранения в базы данных
        """
        with psycopg.connect(host=self.host, dbname=self.db_name, user=self.user, password=self.password,
                             port=self.port, client_encoding=self.encoding) as conn:
            with conn.cursor() as cursor:
                for company in companies:
                    cursor.execute("""
                    INSERT INTO companies (company_id, name, url)
                    VALUES (%s, %s, %s)
                    """, (company.company_id, company.company_name, company.url)
                                   )
                for vacancy in vacancies:
                    cursor.execute("""
                    INSERT INTO vacancies (vacancy_id, company_id, name, city, url, 
                    salary_from, salary_to, requirements)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (vacancy.vacancy_id, vacancy.company_id, vacancy.name, vacancy.city, vacancy.link,
                          vacancy.salary_from, vacancy.salary_to, vacancy.requirements)
                                   )
        conn.close()
