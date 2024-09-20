#!/usr/bin/env python3
"""An Authentication class that inherits from SessionExpAuth"""

from auth.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Storage of the Authentication class"""

    def create_session(self, user_id=None):
        """
        Creates a new session and stores an instance of UserSession

        Args:
            user_id (str): The ID of the user for whom to create a session

        Returns:
            The session ID if seccessful, otherwise None
        """
        if user_id is None:
            return None
        session_id = str(uuid.uuid4())
        user_session = UserSession(user_id=user_id, session_id=session_id)
        self.user_id_by_session_id[session_id] = user_session

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID from the database on the session

        Args:
            session_id (str): The session ID to look up

        Returns:
            str: The User ID if valid, otherwise None
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
        Destroy the session by removing the UserSession from the database
        based on session ID

        Args:
            request (obj): The request object containing the session cookie

        Returns:
            True if session is destroyed, False otherwise
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        try:
            user_session = UserSession.search({"session_id"}): session_id})
        except Exception:
            return False
        if not user_session:
            return False

        try:
            user_session.remove()
            return True
        except Exception:
            return False
