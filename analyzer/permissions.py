from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .exceptions import RateLimitExceeded
from gateway.models import APIKey, KeyBucket
import logging


logger = logging.getLogger(__name__)

class HasEnoughTokens(BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            logger.debug("Non-POST request — skipping token check")
            return True

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            logger.warning("Missing or malformed Authorization header")
            raise PermissionDenied("Invalid or missing API key.")

        api_key_hash = auth_header.removeprefix("Bearer ").strip()

        try:
            api_key = APIKey.objects.get(key_hash=api_key_hash)
            logger.info(f"API key found for hash: {api_key_hash}")
        except APIKey.DoesNotExist:
            logger.error(f"API key not found for hash: {api_key_hash}")
            raise PermissionDenied("API key not recognized.")

        try:
            bucket = KeyBucket.objects.get(api_key=api_key)
            logger.debug(f"Token bucket retrieved: {bucket.remaining_tokens} tokens left")
        except KeyBucket.DoesNotExist:
            logger.critical(f"No token bucket associated with API key: {api_key_hash}")
            raise PermissionDenied("Token bucket missing for API key.")

        if bucket.remaining_tokens < 1:
            logger.warning(f"Rate limit exceeded for API key: {api_key_hash}")
            raise RateLimitExceeded()

        request.token_bucket = bucket
        logger.info(f"Permission granted — {bucket.remaining_tokens} tokens remaining")
        return True