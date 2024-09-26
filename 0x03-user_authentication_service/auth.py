#!/usr/bin/env python3

import bcrypt
from db import DB
from sqlalchemy.orm.session import Session
from uuid import uuid4

from user import Base
from user import User


def _hash_password(password: str) -> bytes:
    """Encrypts a string (password) and returns bytes"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def _generate_uuid() -> str:
    """
    Generates a new UUID and returns it as a string
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes the Auth class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user to the database

        Args:
            email (str): The users email
            password (str): The password of the user

        Returns:
            ValueError: If the user already exists
        """
        user = self._db.find_user_by(email=email)
        if user is not None:
            raise ValueError(f"User {email} already exists")
        hashed_password = _hash_password(password)
        new_user = self.db.add_user(email, hashed_password)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates if the users credentials are correct
        """
        try:
            user = find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                        password.encode("utf-8"),
                        user.hashed_password,
                        )
        except NoResultFound:
            return False
        return False
