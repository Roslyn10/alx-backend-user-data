#!/usr/bin/env python3
"""Adding an expiration Session ID for the API"""

from .session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """A class that inherits from SessionAuth and handles session expiration."""

    def __init__(self):
        """Initializes the class with a session duration."""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session ID for a given user ID,
        including the session's creation time.

        Args:
            user_id (str): The ID of the user for whom to create a session.

        Returns:
            str: The session ID if successful; otherwise, None.
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {  # Fixed typo here
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID for a given session ID,
        considering session duration.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID if valid; otherwise, None.
        """
        if session_id is None:
            return None
        session_data = self.user_id_by_session_id.get(session_id)  # Fixed typo here
        if session_data is None:
            return None
        user_id = session_data.get('user_id')
        created_at = session_data.get('created_at')
        if self.session_duration <= 0:
            return user_id
        if created_at is None:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_id
