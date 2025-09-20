
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.utils import timezone
from .serializers import AnalyzeContentSerializer
from .ai import ModerationService
from .permissions import HasEnoughTokens

class AnalyzeContentViewSet(viewsets.GenericViewSet):
    serializer_class = AnalyzeContentSerializer
    permission_classes = [HasEnoughTokens]

    @action(detail=False, methods=["post"], url_path="content")
    def analyze_content(self, request):

        bucket = getattr(request, "token_bucket")
        bucket.remaining_tokens -= 1
        bucket.last_updated_time = timezone.now()
        bucket.save()

        moderator = ModerationService()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ctype = serializer.validated_data["detected_content_type"]

            content = (
                serializer.validated_data.get("user_input") or
                serializer.validated_data.get("image")
            )
            result = moderator.moderate(content=content, content_type=ctype)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Moderation failed: {str(e)}"},
                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )