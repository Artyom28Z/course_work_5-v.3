class HhVacancy:
    def __init__(self, vacancy_id: int, name: str, company_id: int, city: str, link: str, experience: str,
                 requirements: str, salary_from=0, salary_to=0):
        self.vacancy_id = vacancy_id
        self.name = name
        self.link = link
        self.company_id = company_id
        self.salary_from = salary_from if salary_from else None
        self.salary_to = salary_to if salary_to else None
        self.city = city
        self.experience = experience
        self.requirements = requirements

    @classmethod
    def make_object_list(cls, vacancies: list[dict]) -> list:
        vacancies_list = []
        for vacancy in vacancies:
            temp: HhVacancy = cls(
                vacancy_id=vacancy["id"],
                name=vacancy["name"],
                link=vacancy["alternate_url"],
                company_id=vacancy["employer"]["id"],
                salary_from=vacancy["salary"]["from"] if vacancy["salary"] else 0,
                salary_to=vacancy["salary"]["to"] if vacancy["salary"] else 0,
                city=vacancy["area"],
                experience=vacancy["experience"],
                requirements=vacancy["employment"]
            )
            vacancies_list.append(temp)
        return vacancies_list
