class HhCompany:
    def __init__(self, company_id: int, company_name: str, url: str):
        self.company_id = company_id
        self.company_name = company_name
        self.url = url

    @classmethod
    def company_list(cls, companies: list[dict]):
        """Класс-метод критериев компании
        """
        company_list: list = []
        company_ids = set()
        for company in companies:
            if company["employer"]["id"] not in company_ids:
                temp: HhCompany = cls(
                    company_id=company["employer"]["id"],
                    company_name=company["employer"]["name"],
                    url=company["employer"]["alternate_url"],
                    )
                company_list.append(temp)
                company_ids.add(company["employer"]["id"])
        return company_list
