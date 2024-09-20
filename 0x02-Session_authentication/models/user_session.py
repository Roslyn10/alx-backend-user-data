#!/usr/bin/env python3
"""A Model and userSession that inherits from Base"""

from models.base import Base


class UserSession(Base):
    """A user session that inherits from base"""

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes the user class

        Args:
            *args: Variable length argument list
            **kwargs: Keyword arguments
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id', None)
        self.session_id = kwards.get('session_id', None)
