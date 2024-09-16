#!/usr/bin/env puython3
""" A module that is used to check authentication of users """


from flask import request
from typing import List, TypeVar


class Auth:
    """A class that checks authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if a path requires authentication"""
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header from the request """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user based on the request"""
        return None
