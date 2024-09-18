#!/usr/bin/env python3
"""Session Authentication"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Class to handle session-based authentication, inheriting from Auth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given 'user_id'

        Args:
            user_id (str): The ID of the user for who the session is being created

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
            str: The User ID associated with the session ID, or None if the session ID is valid or not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
