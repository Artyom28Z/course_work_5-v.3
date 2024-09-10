from abc import ABC, abstractmethod


import requests
from requests import Response, JSONDecodeError


class Api(ABC):
    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @abstractmethod
    def _get_response(self) -> Response:
        pass

    @abstractmethod
    def get_vacancies(self) -> list[dict]:
        pass

    @staticmethod
    @abstractmethod
    def _check_status(response) -> bool:
        pass


class HhApi(Api):
    def __init__(self) -> None:
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {
            "area": 113,
            "page": 0,
            "per_page": 100,
            "employer_id": ["9498120",
                            "5920492",
                            "64174",
                            "87821",
                            "15478",
                            "1375441",
                            "598471",
                            "633069",
                            "139",
                            "4496"]
        }
        self.__vacancies = []

    @property
    def url(self) -> str:
        """Метод возвращающий ссылку для подключения
        """
        hh_url = "https://api.hh.ru/vacancies"
        return hh_url

    def _get_response(self) -> Response:
        """Метод подключения к API HeadHunter
        """
        return requests.get(self.url, headers=self.headers, params=self.__params)

    def get_vacancies(self) -> None:
        """Метод создания списка словарей с вакансиями
        """
        response = self._get_response()
        is_allowed = self._check_status(response)
        #if not is_allowed:
            #raise HhApiException(f"Ошибка запроса. Status code: {Response.status_code}")
        #try:
        if is_allowed:
            while self.__params.get("page") != 20:
                response = self._get_response()
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1
        #except JSONDecodeError:
            #raise HhApiException("Ошибка получения данных")

    @property
    def vacancies(self):
        """Геттер списка вакансий
        """
        return self.__vacancies

    @staticmethod
    def _check_status(response: Response) -> bool:
        """Статический метод проверки подключения
        """
        return response.status_code == 200
