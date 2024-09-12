#!/usr/bin/env python3
"""A module that encrypts users passwords"""


import bcrypt

def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("UTF-8"), salt)
