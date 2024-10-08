Курсовая 5. Работа с базами данных

Для запуска проекта необходимо установить библиотеку базовой версии. Версии зависимостей указаны в файле pyproject.toml.

Также для запуска проекта необходимо указать свои параметры: пароль, хост, имя пользователя, имя базы данных, имя создаваемой базы данных, кодировка и порт(если они отличатся) в файле config.py.


В рамках проекта получаем данные о компаниях и вакансиях с сайта hh.ru, проектируем таблицы в БД PostgreSQL и загружаем полученные данные в созданные таблицы.

Основные этапы проекта:

Получаем данные о работодателях и их вакансиях с сайта hh.ru. Для этого воспользуйтесь публичным API hh.ru и запросами контента

Выбираем не менее 10 интересных компаний, от которых вы будете получать данные о вакансиях по API. Спроектировать таблицы в БД PostgreSQL для хранения данных о работодателях и их вакансиях. Для работы с БД включаем поддержку psycopg2

Реализуем код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.

Создаём класс DBManager для работы с данными в БД.

Создаём класс DBManager, который будет подключаться к БД PostgreSQL и иметь следующие методы:

get_companies_and_vacancies_count() — получает список всех компаний и количество вакансий в каждой компании.

get_all_vacancies() — получает список всех вакансий с указанием названия компании, названия вакансий и зарплат и ссылок на вакансии.

get_avg_salary() — получает среднюю зарплату по вакансиям.

get_vacancies_with_higher_salary() — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

get_vacancies_with_keyword() — список получает все вакансии, в названии которых представлены переданные в методе слова, например python.

*Класс DBManager будет использовать библиотеку psycopg2 для работы с БД.
