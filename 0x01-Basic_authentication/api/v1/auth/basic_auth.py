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
