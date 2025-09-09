from django.contrib import admin
from .models import APIKey, KeyBucket, RequestLog

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['key_name', 'owned_by', 'is_active_key', 'key_hash']
    list_editable = ['is_active_key']

@admin.register(KeyBucket)
class KeyBucketAdmin(admin.ModelAdmin):
    list_display = ['api_key', 'remaining_tokens', 'last_updated_time']
    list_editable = ['remaining_tokens']


@admin.register(RequestLog)
class KeyBucketAdmin(admin.ModelAdmin):
    list_display = ['key', 'path', 'method', 'status_code', 'duration']
