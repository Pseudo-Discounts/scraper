from scraper.core.dto.dto import ErrorType, ProductLink, ProductDetails
from scraper.core.service.factory import MarketplaceFactory, OzonFactory


class ScraperPipelineService:
    """
        Класс, отвечающий за процесс получения "полезных" данных о товаре по ссылке на него.
    """

    def __init__(self):
        # Регистрируем реализации фабрик для ссылок на маркетплейсы.
        self.__factories = {"ozon.ru": OzonFactory}

    def handle(self, link: ProductLink) -> ProductDetails:
        """
            Здесь мы просто по очереди вызываем реализации ``ProductWebDataPuller`` и ``ProductDetailsScraper``.
        """

        factory = self.__get_factory_by_link(link)
        if factory is None:
            return ProductDetails(ErrorType.MARKETPLACE_NOT_SUPPORTED, None, None, None, None, None)

        web_data = factory.get_product_web_data_puller().get_web_data(link)
        details = factory.get_product_details_scraper().get_details(web_data)
        return details

    def __get_factory_by_link(self, link: ProductLink) -> MarketplaceFactory | None:
        """
            Получение конкретной реализации фабрики по ссылке на маркетплейс.
        """

        for l, f in self.__factories.items():
            if l in link.link:
                return f()

        return None
