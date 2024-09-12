#!/usr/bin/env python3
""" A module"""

import re
from typing import List
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """A function that returns the log message obfuscated

    Args:
        fields: list of strings representing all fields to obfuscate
        redaction: str representing by what the field will be obfuscated
        message: str representing log line
        separator: str representing by which character is seperating all fields
                in the log line(message)

    """
    pattern = f"({'|'.join(fields)})=([^ {separator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incomging log records using filter_datum"""
        ori_mess = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            ori_mess, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a logging.logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    c_handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)

    c_handler.setFormatter(formatter)
    logger.addHandler(c_handler)
    return logger
