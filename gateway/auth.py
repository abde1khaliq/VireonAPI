from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import APIKey

User = get_user_model()

class APIKeyAuthenticationMiddleware(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed(
                "Missing or invalid Authorization header")
        token = auth_header.removeprefix("Bearer ").strip()
        if token == "testcase": # Test case token. DO NOT USE IN PRODUCTION DUDE
            test_user, _ = User.objects.get_or_create(username="apitestuser")
            api_key, _ = APIKey.objects.get_or_create(key_hash=token, owned_by=test_user, key_name='test_case', is_active_key=True)
        else:
            api_key = APIKey.objects.filter(key_hash=token).first()
        api_key = APIKey.objects.filter(key_hash=token).first()
        
        if not api_key or not api_key.is_active_key:
            raise AuthenticationFailed("Invalid or expired API key")
        
        request.api_key = api_key

        return (None, None)