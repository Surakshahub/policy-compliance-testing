import logging

logging.basicConfig(
    filename="ai_service.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


class LoggerService:

    @staticmethod
    def log_info(message):

        logging.info(message)

    @staticmethod
    def log_error(message):

        logging.error(message)