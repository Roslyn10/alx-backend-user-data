#!/usr/bin/env python3
"""An authentication class that manages user sessions using database storage,
inheriting from SessionExpAuth."""

from auth.auth.session_exp_auth import SessionExpAuth
import uuid
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session-based authentication class that uses a database
    to manage session storage."""

    def create_session(self, user_id=None):
        """
        Creates a new session and stores an instance
        of UserSession in the database.

        Args:
            user_id (str): The ID of the user for whom to create a session.

        Returns:
            The session ID if successful, otherwise None.
        """
        if user_id is None:
            return None
        session_id = str(uuid.uuid4())
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        self.user_id_by_session_id[session_id] = user_session
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with the given session ID
        by querying the database.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            The user ID if the session is valid and found, otherwise None.
        """
        if session_id is None:
            return None
        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if not user_session:
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroys the session by removing the corresponding UserSession from
        the database based on the session ID.

        Args:
            request (obj): The request object containing the session cookie.

        Returns:
            True if the session is successfully destroyed, False otherwise.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        if not user_session:
            return False

        try:
            user_session.remove()
            return True
        except Exception:
            return False
