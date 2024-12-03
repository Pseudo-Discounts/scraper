import json
from curl_cffi import requests
from abc import ABC, abstractmethod

from scraper.core.dto.dto import ProductLink, ProductWebData, WebDataType


class ProductWebDataPuller(ABC):
    """
        Интерфейс, от которого должны наследоваться классы, отвечающие за
        "вытягивание" HTML разметки со страниц с товарами (или JSON-ов с информацией о товарах).
    """

    @abstractmethod
    def get_web_data(self, link: ProductLink) -> ProductWebData:
        """
            Абстрактный метод, принимающий ссылку на товар и
            возвращающий полученную по этой ссылке разметку со страницы товара.
        """

        pass


class OzonProductWebDataPuller(ProductWebDataPuller):
    """
        Реализация интерфейса ``ProductWebDataPuller``.
        Отвечает за получения текста в формате JSON с различной информацией о товаре с сайта Ozon.
    """

    def get_web_data(self, link: ProductLink) -> ProductWebData:
        return self.__get_json(link)

    def __get_json(self, link: ProductLink) -> ProductWebData:
        # Для выполнения запросов используем библиотеку curl_cffi (так не срабатывает защита Ozon от ботов).
        session = requests.Session()
        raw_data = session.get("https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=" + link.link)
        is_adults_only = False

        # Если товар имеет ограничение по возрасту, отправляем запрос повторно, но с дополнительными куками.
        json_data = json.loads(raw_data.content.decode())
        if json_data["layout"][0]["component"] == "userAdultModal":
            is_adults_only = True
            cookies = {"is_adult_confirmed": "true", "adult_user_birthdate": "2000-10-10"}
            raw_data = session.get(
                "https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=" + link.link,
                cookies=cookies
            )

        session.close()

        return ProductWebData(link, raw_data.content.decode(), WebDataType.JSON, is_adults_only)
