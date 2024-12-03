import logging

from scraper.core.service.broker import MessageBrokerService


def configure_logger():
    """
        Задаем базовое логирование в терминал.
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d %(levelname)-8s %(name)-5s %(filename)-10s (%(lineno)03d) : %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
        handlers=[logging.StreamHandler()]
    )


def main():
    """
        Точка входа в скрипт.
        Конфигурируем логгер и запускаем приём сообщений из брокера сообщений.
    """

    configure_logger()

    broker = MessageBrokerService()
    broker.consume()


if __name__ == "__main__":
    main()
