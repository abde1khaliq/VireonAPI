from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
import secrets

User = get_user_model()


class APIKey(models.Model):
    key_hash = models.CharField(max_length=100, editable=False, unique=True)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    key_name = models.CharField(max_length=100)
    is_active_key = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key_hash:
            self.key_hash = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'Key name: {self.key_name} Owner: ({self.owned_by.username})'


class RequestLog(models.Model):
    key = models.ForeignKey('APIKey', on_delete=models.SET_NULL, null=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.method} {self.path} via {self.key}"


class KeyBucket(models.Model):
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE)
    remaining_tokens = models.PositiveIntegerField(default=1000)
    last_updated_time = models.DateTimeField(auto_now=True)
    max_token_limit = models.PositiveIntegerField(default=1000)

    def __str__(self) -> str:
        return f'Key bucket for {self.api_key} with {self.remaining_tokens} tokens left'
