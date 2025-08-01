from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomSessionAuthentication(SessionAuthentication):
    """
    Custom session authentication that can be extended if needed.
    """

    pass


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that can be extended if needed.
    """

    pass
