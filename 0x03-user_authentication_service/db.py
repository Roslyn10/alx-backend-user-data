#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database

        Args:
            email (str): The user's email
            hashed_password (str): The hashed password of the user

        Returns:
            User: The newly created user object
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        return new_user


    def find_user_by(self, **kwargs):
        """
        Finds a user in the database by arbitrary keyword arguments

        Args:
            **kwargs: Arbitrary keywords arguments corresponding
            to User attributes

        Returns:
            User: The user found that matches the given criteria
        """
        if not kwargs:
            raise InvalidRequestError

        column_name = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_name:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user in the database

        Args:
            user_id (int): The ID of the user to update
            kwargs: Key-value pairs of attributes to updates

        Raises:
            ValueError: If any of the kwargs do not correspond to a value
            NoResultFound: If no user with the given user_id is found
            InvalidRequestError: If there is an invalid request
            with the database
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"User has no attribute '{key}'")
            self._session.commit()
