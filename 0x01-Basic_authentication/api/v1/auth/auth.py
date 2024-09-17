#!/usr/bin/env puython3
""" A module that is used to check authentication of users """


from flask import request
from typing import List, TypeVar


class Auth:
    """A class to handle authentication process

    Provides methods to determine if a request requires authentication,
    extract the authorization header from an HTTP request,
    and retrieve the current user
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a specific path requires authentication

        Args:
            path (str): The path of the request to check for authentication.
            excluded_paths (List[str]): A list of paths that
            do not require authentication.

        Return:
            bool: True if the path requires authentication,
            False if it is in excluded paths
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the 'Authorization' header from an HTTP request

        Args:
            request (Optional): The HTTP request object that may contain
            the 'Authorization' header

        Returns:
            str: The value of the 'Authorization' header if it exists,
            otherwise None.
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request

        Args:
            request (Optional): The HTTP request object used to
            determine the current user.

        Return:
            TypeVar('User'): The current user instance if identified,
            otherwise None.
        """
        return None
