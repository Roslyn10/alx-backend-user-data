#!/usr/bin/env python3
"""Session Authentication"""

from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Class to handle session-based authentication, inheriting from Auth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given 'user_id'

        Args:
            user_id (str): The ID of the user for who
            the session is being created

        Return:
            The generated session ID as a string
            Returns None if `user_id` is None or not a string
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the User ID associated with a given Session ID

        Args:
            Session_id (str): The session ID to look up. Defaults to None

        Return:
            str: The User ID associated with the session ID,
            or None if the session ID is valid or not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a cookie value

        Args:
            The incoming HTTP request

        Return:
            User: The User instance if found. otherwise None
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Destroys the session for the user

        Args:
            The request object containing the session

        Return:
            True if the session was successfully destroyed,
            False if not
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_for_session_id(session_id)
        if not user_id:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True

        return False
