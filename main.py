from src.api import HhApi
from src.company import HhCompany
from src.db_creator import DbCreator
from src.db_manager import DbManager
from src.vacancy import HhVacancy
from config import host, database, user, password, port, encoding, db_name


def main():
    api = HhApi()
    api.get_vacancies()
    vac = HhVacancy.make_object_list(api.vacancies)
    com = HhCompany.company_list(api.vacancies)

    db_cr = DbCreator(host, database, user, password, port, encoding, db_name)
    db_cr.create_database()
    db_cr.create_tables()
    db_cr.save_data_to_db(vac, com)
    db_mn = DbManager(host, database, user, password, port, encoding, db_name)

    while True:
        user_input = input(f"|1| Показать количество вакансий компаний\n"
                           f"|2| Показать все вакансии\n"
                           f"|3| Посчитать среднюю зарплату\n"
                           f"|4| Показать все вакансии с зарплатой выше средней\n"
                           f"|5| Вывести вакансии по ключевому слову\n"
                           f"|0| Закрыть программу\n"
                           f"""Для выбора - вводите цифру, далее ENTER
""")

        if user_input == "1":
            for ind in db_mn.get_companies_end_vacancies_count():
                print(ind)

        elif user_input == "2":
            for ind in db_mn.get_all_vacancies():
                print(ind)

        elif user_input == "3":
            print(f"Средняя зарплата: {db_mn.get_avg_salary()[0][0]} рублей")

        elif user_input == "4":
            for ind in db_mn.get_vacancies_with_higher_salary():
                print(ind)

        elif user_input == "5":
            user_keyword = input("Введите ключевое слово для поиска\n")
            for ind in db_mn.get_vacancies_with_keyword(user_keyword):
                print(ind)

        elif user_input == "0":
            exit()


if __name__ == '__main__':
    main()
