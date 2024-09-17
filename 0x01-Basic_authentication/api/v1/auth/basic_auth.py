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

        """
        if authorization_header is None:
            return None
        if authorization_header is not str:
            return None
        if 'Basic' not in authorization_header:
            return None
        return [6:]
