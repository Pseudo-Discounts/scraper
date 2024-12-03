import re
import json
from decimal import Decimal
from abc import ABC, abstractmethod

from scraper.core.dto.dto import ErrorType, WebDataType, ProductWebData, ProductDetails, ProductLink


class ProductDetailsScraper(ABC):
    """
        Интерфейс, от которого должны наследоваться классы, отвечающие за
        получение "полезных" данных с пришедшей на вход HTML разметки (или JSON-а)
    """

    @abstractmethod
    def get_details(self, web_data: ProductWebData) -> ProductDetails:
        """
            Абстрактный метод, принимающий на вход "вытянутые" по ссылке данные и
            возвращающий "полезные" данные о товаре (например: название товара, цена на товар и т. д.)
        """

        pass


class OzonProductDetailsScraper(ProductDetailsScraper):
    """
        Реализация интерфейса ``ProductDetailsScraper``.
        Отвечает за получение "полезных" данных о товаре на Ozon.
    """

    def get_details(self, web_data: ProductWebData) -> ProductDetails:
        if web_data.web_data_type == WebDataType.JSON:
            return self.__get_details_from_json(web_data)

    def __get_details_from_json(self, web_data: ProductWebData) -> ProductDetails:
        json_data = json.loads(web_data.web_data)

        name = json_data["seo"]["title"]
        match = re.match(r"^(.*?)\s+купить на OZON по низкой цене", name)
        if match:
            name = match.group(1)

        price = Decimal(json.loads(json_data["seo"]["script"][0]["innerHTML"])["offers"]["price"])

        image_link = ProductLink(json.loads(json_data["seo"]["script"][0]["innerHTML"])["image"])

        return ProductDetails(ErrorType.NONE, name, price, web_data.is_adults_only, image_link, web_data.product_link)
