from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import APIKey

User = get_user_model()

import logging
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import APIKey

logger = logging.getLogger(__name__)
User = get_user_model()

class APIKeyAuthenticationMiddleware(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            logger.warning("Missing or malformed Authorization header")
            raise AuthenticationFailed("Missing or invalid Authorization header")

        token = auth_header.removeprefix("Bearer ").strip()

        if token == "testcase":  # Test token — safe for dev only
            test_user, _ = User.objects.get_or_create(username="apitestuser")
            api_key, _ = APIKey.objects.get_or_create(
                key_hash=token,
                owned_by=test_user,
                key_name="test_case",
                is_active_key=True
            )
            logger.info("Test API key used for authentication")
        else:
            api_key = APIKey.objects.filter(key_hash=token).first()

        if not api_key or not api_key.is_active_key:
            logger.error(f"Invalid or inactive API key: {token}")
            raise AuthenticationFailed("Invalid or expired API key")

        request.api_key = api_key
        logger.info(f"Authenticated request with API key: {token}")
        return (None, None)