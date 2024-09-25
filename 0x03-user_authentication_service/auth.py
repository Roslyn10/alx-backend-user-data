#!/usr/bin/env python3

import bcrypt


def _hash_password(password: str) -> bytes:
    """Encrypts a string (password) and returns bytes"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash
