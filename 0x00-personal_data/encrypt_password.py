#!/usr/bin/env python3
"""A module that encrypts users passwords"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("UTF-8"), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that a provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
