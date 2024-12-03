import json
from enum import Enum
from typing import Any
from decimal import Decimal
from dataclasses import asdict

from scraper.core.dto.dto import ProductDetails


class ProductDetailsSerializer:
    """
        Класс, отвечающий за сериализацию объектов класса
        ``ProductDetails`` в JSON (для последующей передачи в другое приложение).
    """

    @staticmethod
    def to_json(product_details: ProductDetails) -> str:
        """
            Сериализация объекта класса ``ProductDetails`` в JSON.
        """

        product_details_dict = asdict(product_details)

        def custom_serializer(obj: Any) -> Any:
            if isinstance(obj, Decimal):
                return str(obj)
            if isinstance(obj, Enum):
                return obj.value
            return obj

        return json.dumps(product_details_dict, default=custom_serializer, indent=4)
