#!/usr/bin/env python3
"""A BAsic Authentication"""

from api.v1.auth.auth import Auth
import base64
from base64 import decode, b64decode
from models.user import User


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
        if not isinstance(base64_authorization_header, str) is None:
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
        if not isinstance(decoded_base64_authorization_header, str) is None:
            return (None, None)
        if ":" in decoded_base64_authorization_header:
            return (None, None)

        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)
