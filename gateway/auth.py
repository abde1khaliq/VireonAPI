from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed(
                "Missing or invalid Authorization header")
        token = auth_header.removeprefix("Bearer ").strip()
        api_key = APIKey.objects.filter(key_hash=token).first()
        
        if not api_key or not api_key.is_active_key:
            raise AuthenticationFailed("Invalid or expired API key")
        
        request.api_key = api_key

        return (None, None)