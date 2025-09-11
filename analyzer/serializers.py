from rest_framework import serializers

class AnalyzeContentSerializer(serializers.Serializer):
    user_input = serializers.CharField(required=False)