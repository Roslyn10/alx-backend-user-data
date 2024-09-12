#!/usr/bin/env python3
""" A module"""

import re


def filter_datum(fields, redaction, message, separator):
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
