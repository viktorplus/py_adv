from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer
from .tokens import REFRESH_COOKIE, set_auth_cookies, delete_auth_cookies


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        set_auth_cookies(response, response.data['access'], response.data['refresh'])
        return response


class RefreshTokenMixin:
    def validate_refresh(self, request):
        refresh = request.data.get('refresh') or request.COOKIES.get(REFRESH_COOKIE)
        serializer = self.get_serializer(data={'refresh': refresh})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as error:
            raise InvalidToken(error.args[0])
        return serializer.validated_data


class RefreshView(RefreshTokenMixin, TokenRefreshView):
    def post(self, request, *args, **kwargs):
        tokens = self.validate_refresh(request)
        response = Response(tokens, status=status.HTTP_200_OK)
        set_auth_cookies(response, tokens['access'], tokens.get('refresh'))
        return response

class LogoutView(RefreshTokenMixin, TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        self.validate_refresh(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        delete_auth_cookies(response)
        return response