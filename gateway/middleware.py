from .models import APIKey, RequestLog
import datetime
import logging

logger = logging.getLogger(__name__)

class CaptureKeyedRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = datetime.datetime.now()
        path = request.path

        try:
            response = self.get_response(request)
        except Exception as view_error:
            logger.critical(f"🚨 Error during view execution: {view_error}", exc_info=True)
            raise

        end = datetime.datetime.now()
        duration = end - start

        try:
            if path == "/v1/analyze/content/" and request.method == "POST":
                auth_header = request.headers.get("Authorization", "")
                if auth_header.startswith("Bearer "):
                    api_key_raw = auth_header.split("Bearer ")[1].strip()
                    key_obj = APIKey.objects.filter(key_hash=api_key_raw).first()

                    if key_obj:
                        RequestLog.objects.create(
                            key=key_obj,
                            path=path,
                            method=request.method,
                            status_code=response.status_code,
                            ip_address=request.META.get("REMOTE_ADDR"),
                            duration=duration,
                        )
                        logger.info(f"Logged request for API key: {api_key_raw} — {duration.total_seconds()}s")
                    else:
                        logger.warning(f"No matching API key found for hash: {api_key_raw}")
                else:
                    logger.warning("Authorization header missing or malformed")
        except Exception as middleware_error:
            logger.error(f"🚨 Middleware logging error: {middleware_error}", exc_info=True)

        return response