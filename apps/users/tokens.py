from django.conf import settings
from rest_framework_simplejwt.settings import api_settings


ACCESS_COOKIE = 'access_token'
REFRESH_COOKIE = 'refresh_token'


def set_auth_cookies(response, access, refresh=None):
    _set_cookie(response, ACCESS_COOKIE, access, api_settings.ACCESS_TOKEN_LIFETIME)
    if refresh:
        _set_cookie(response, REFRESH_COOKIE, refresh, api_settings.REFRESH_TOKEN_LIFETIME)


def delete_auth_cookies(response):
    response.delete_cookie(ACCESS_COOKIE, samesite='Lax')
    response.delete_cookie(REFRESH_COOKIE, samesite='Lax')

def _set_cookie(response, name, value, lifetime):
    response.set_cookie(
        name,
        value,
        max_age=int(lifetime.total_seconds()),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
    )