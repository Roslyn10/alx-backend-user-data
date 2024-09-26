#!/usr/bin/env python3

import bcrypt
from db import DB
from sqlalchemy.orm.session import Session
from uuid import uuid4
from typing import Union

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

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user and returns the session ID

        Args:
            email (str): The email of the user

        Returns:
            str: The session ID

        Raises:
            NoResultFound: If the user is no found in the database
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        takes a session_id string argument and returns the corresponding user
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.fid_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(sef, user_id: int) -> None:
        """
        Destroys a session
        """
        if user_id is None:
            return None
        self._db.update_uer(user_id, session_i=None)
