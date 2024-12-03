from enum import Enum
from decimal import Decimal
from dataclasses import dataclass


class ErrorType(Enum):
    """
        Тип ошибки, произошедшей в процессе получения данных с маркетплейса.
    """

    # Если успешно получили информацию о товаре, то должен быть выставлен этот тип ошибки.
    NONE = "NONE"

    # Если пришла ссылка на маркетплейс, логика для которого не реализована, то должна быть выставлена эта ошибка.
    MARKETPLACE_NOT_SUPPORTED = "MARKETPLACE_NOT_SUPPORTED"


class WebDataType(Enum):
    """
        Вид данных, который отдает маркетплейс.
    """

    HTML = "HTML"
    JSON = "JSON"


@dataclass(frozen=True)
class ProductLink:
    """
        Обёртка для ссылок.
    """

    link: str


@dataclass(frozen=True)
class ProductWebData:
    """
        Данные, полученные от маркетплейса.
    """

    # Ссылка на сам товар на маркетплейсе.
    product_link: ProductLink

    # Полученные от маркетплейса данные в формате ``web_data_type`` (см. ниже).
    web_data: str

    # Вид данных, который отдает маркетплейс.
    web_data_type: WebDataType

    # Имеет ли товар ограничение по возрасту.
    is_adults_only: bool


@dataclass(frozen=True)
class ProductDetails:
    """
        "Полезная" информация о товаре.
    """

    # Тип ошибки, произошедшей во время получения данных с маркетплейса.
    error_type: ErrorType

    # Название товара.
    name: str | None

    # Цена на товар.
    price: Decimal | None

    # Имеет ли товар ограничение по возрасту.
    is_adults_only: bool | None

    # Ссылка на изображение товара.
    image_link: ProductLink | None

    # Ссылка на сам товар на маркетплейсе.
    product_link: ProductLink | None
