
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
import logging

logger = logging.getLogger(__name__)

class AnalyzeContentViewSet(viewsets.GenericViewSet):
    serializer_class = AnalyzeContentSerializer
    permission_classes = [HasEnoughTokens]

    @action(detail=False, methods=["post"], url_path="content")
    def analyze_content(self, request):
        logger.info("Received content analysis request")

        moderator = ModerationService()
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            logger.info("Request data validated successfully")
        except Exception as validation_error:
            logger.warning(f"Validation failed: {validation_error}")
            return Response(
                {"error": f"Validation error: {str(validation_error)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ctype = serializer.validated_data["detected_content_type"]
            content = (
                serializer.validated_data.get("user_input") or
                serializer.validated_data.get("image")
            )
            logger.info(f"Detected content type: {ctype}")
            logger.debug(f"Content payload: {content}")

            result = moderator.moderate(content=content, content_type=ctype)
            logger.info("Moderation completed successfully")

            # Only subtract token if moderation succeeds
            try:
                bucket = getattr(request, "token_bucket")
                logger.info(f"User token bucket before deduction: {bucket.remaining_tokens}")
                bucket.remaining_tokens -= 1
                bucket.last_updated_time = timezone.now()
                bucket.save()
                logger.info(f"Token deducted. Remaining tokens: {bucket.remaining_tokens}")
            except Exception as token_error:
                logger.critical(f"Failed to update token bucket: {token_error}")

            return Response(result, status=status.HTTP_200_OK)

        except Exception as moderation_error:
            logger.error(f"Moderation failed: {moderation_error}")
            return Response(
                {"error": f"Moderation failed: {str(moderation_error)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )