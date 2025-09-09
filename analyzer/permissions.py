from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .exceptions import RateLimitExceeded
from gateway.models import APIKey, KeyBucket


class HasEnoughTokens(BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return True

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise PermissionDenied("Invalid or missing API key.")

        api_key_hash = auth_header.removeprefix("Bearer ").strip()
        api_key = APIKey.objects.get(key_hash=api_key_hash)
        bucket = KeyBucket.objects.get(api_key=api_key)

        if bucket.remaining_tokens < 1:
            raise RateLimitExceeded()

        request.token_bucket = bucket
        return True
