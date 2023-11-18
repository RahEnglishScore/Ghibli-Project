from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class GhibliApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get("Ghiblikey")
        if api_key != settings.GHIBLI_API_KEY:
            raise AuthenticationFailed("No or invalid API key provided")
        return (None, None)
