import psycopg

from src.company import HhCompany
from src.vacancy import HhVacancy


class DbCreator:
    # def __init__(self, dbname, params):
    #     self.dbname = dbname
    #     self.params = params
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    #(host=self.host, dbname=self.database, user=self.user, password=self.password, port=self.port)

    def create_database(self):
        conn = psycopg.connect(host=self.host, dbname=self.database, user=self.user, password=self.password,
                               port=self.port)
        #conn.set_client_encoding('UTF8')
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(f"""UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'postgres'""")
            cursor.execute(f"""SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity
                           WHERE pg_stat_activity.datname = 'postgres' AND pid <> pg_backend_pid()""")
            cursor.execute(f'DROP DATABASE IF EXISTS postgres')
            cursor.execute(f"""CREATE DATABASE postgres
                               WITH
                               OWNER = 'postgres'
                               ENCODING = 'UTF8'""")
        conn.close()

    def save_data_to_db(self, vacancies: list[HhVacancy], companies: [HhCompany]):
        with psycopg.connect(host=self.host, dbname=self.database, user=self.user, password=self.password,
                             port=self.port) as conn:
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
                    """, (vacancy.vacancy_id, vacancy.company_id, vacancy.name, vacancy.city, vacancy.url,
                          vacancy.salary_from, vacancy.salary_to, vacancy.requirements)
                                   )
        conn.close()

    def create_tables(self):
        with psycopg.connect(host=self.host, dbname=self.database, user=self.user, password=self.password,
                             port=self.port) as conn:
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
