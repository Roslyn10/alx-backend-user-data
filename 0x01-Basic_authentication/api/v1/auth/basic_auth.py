#!/usr/bin/env python3
"""A BAsic Authentication"""

from api.v1.auth.auth import Auth
import base64


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
        Returns the decoded value of a Base64 string base64_authorization_header

        Args:
            base64_authorization_header (str): The Base64 encoded string

        Return:
            str: The decoded value as a UTF-8 string if valid,
            otherwise None.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header) is None:
            return None
        try:
            base64_bytes = base64.b64decode(base64_authorization_header, validate=True)
            decoded_str = base64_bytes.decode('utf-8')
            return decoded_str
        except Exception
            return None

