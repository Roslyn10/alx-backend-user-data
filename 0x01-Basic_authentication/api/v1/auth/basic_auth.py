#!/usr/bin/env python3
"""A BAsic Authentication"""

from api.v1.auth.auth import Auth
import base64
from base64 import decode, b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Inherits from auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header
        of a Basic Authentication

        Args:
            authorization_header (str): The full Authorization header

        Return:
            str: The Base64 part of the Authorization header if it is valid,
            otherwise None
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        Returns the decoded value of a Base64
        string base64_authorization_header

        Args:
            base64_authorization_header (str): The Base64 encoded string

        Return:
            str: The decoded value as a UTF-8 string if valid,
            otherwise None.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            b64 = base64_authorization_header.encode('utf-8')
            b64 = base64.b64decode(b64)
            decoded_str = b64.decode('utf-8')
            return decoded_str
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value

        Args:
           decoded_base64_authoriization_header(str): The Base64 decoded string

        Returns:
            tuple: A tuple containing the user email and password.
                    Returns (None, None) if the input is invalid
                    or doesnt contain ':'.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" in decoded_base64_authorization_header:
            return (None, None)

        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """
        Returns the User instance based on their email and password

        Args:
            user_email (str): The user's email address
            user_pwd (str): The user's password

        Returns:
            User: The user instance if found and valid, otherwise None
        """
        if user_email is not isinstance(user_email, str):
            return None
        if user_email is None:
            return None
        if user_pwd is not isinstance(user_pwd, str) and user_pwd is None:
            return None
        try:
            user = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Auth and retrieves the User instance for a request

        Args:
            request: The HTTP request object

        Returns:
            User: The User instance is authentication is successful,
            otherwise None
        """
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        decoded_auth = self.decode_base64_authorization_header(b64_auth_header)
        email, password = self.extract_user_credentials(decoded_auth)
        return self.user_object_from_credentials(email, password)
