import psycopg


class DbManager:
    # def __init__(self, dbname, params):
    #     self.dbname = dbname
    #     self.params = params
    #     (database=self.dbname, **self.params)

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        #(host=self.host, database=self.database, user=self.user, password=self.password, port=self.port)

    def get_companies_end_vacancies_count(self):
        """Метод создания списка всех компаний и колечества вакансий у каждой компании
        """
        conn = psycopg.connect(host=self.host, dbname=self.database, user=self.user, password=self.password,
                               port=self.port)
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT companies.name, COUNT(*) AS vacancies_count
            FROM companies
            JOIN vacancies USING (company_id)
            GROUP BY companies.name
            """)
            result = cursor.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self):
        """Метод создания списка вакансий с указанием компании, вакансии, зарплаты и ссылки
        """
        with psycopg.connect(host=self.host, dbname=self.database, user=self.user, password=self.password,
                             port=self.port) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT companies.name, vacancies.name, salary_from, salary_to, vacancies.url 
                FROM vacancies
                JOIN companies USING (company_id) 
                """)
                result = cursor.fetchall()
        conn.close()
        return result

    def get_avg_salary(self):
        """Метод получения средней зарплаты
        """
        with psycopg.connect(host=self.host, dbname=self.database, user=self.user, password=self.password,
                             port=self.port) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT CAST(AVG(salary_from) as INT) 
                FROM vacancies
                """)
                result = cursor.fetchall()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """Метод создания списка вакансий с зарплатой выше средней
        """
        with psycopg.connect(host=self.host, dbname=self.database, user=self.user, password=self.password,
                             port=self.port) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                                SELECT * FROM vacancies
                                WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
                                ORDER BY salary_from DESC
                                """)
                result = cursor.fetchall()
            conn.close()
            return result

    def get_vacancies_with_keyword(self, keyword: str):
        """Метод создания списка вакансий, в которых содержится введенное ключевое слово
        """
        with psycopg.connect(host=self.host, dbname=self.database, user=self.user, password=self.password,
                             port=self.port) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                SELECT * FROM vacancies
                WHERE name LIKE '%{keyword}%' OR requirements LIKE '%{keyword}%'
                ORDER BY salary_from DESC
                """)
                result = cursor.fetchall()
        conn.close()
        return result
