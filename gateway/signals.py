from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import APIKey, KeyBucket

@receiver(post_save, sender=APIKey)
def generate_token_bucket_for_key(sender, instance, created, **kwargs):
    if created:
        KeyBucket.objects.create(api_key=instance)