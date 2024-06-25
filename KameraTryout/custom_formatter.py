"""
Created by Fabian Gnatzig in 2024
Contact: fabiangnatzig@gmx.de
"""
import logging

# https://betterstack.com/community/questions/how-to-color-python-logging-output/


class CustomFormatter(logging.Formatter):
    """
    Custom formater for colored logging.
    """
    white = "\u001b[37m"
    light_white = "\u001b[1m"
    yellow = "\u001b[33m"
    red = "\u001b[31m"
    bold_red = "\u001b[31m\u001b[1m"
    reset = "\u001b[0m"
    log_format = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: white + log_format + reset,
        logging.INFO: light_white + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset
    }

    def format(self, record):
        """
        Formats the record.
        :param record: The incoming record that should log.
        :return: The formated record.
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
