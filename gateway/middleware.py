import datetime
import logging
from .models import APIKey, RequestLog

logger = logging.getLogger(__name__)

class CaptureKeyedRequestMiddleware:
    def __init__(self, get_response): 
        self.get_response = get_response

    def __call__(self, request):
        start = datetime.datetime.now()
        try:
            response = self.get_response(request)
        except Exception as view_error:
            print(f"🚨 Error during view execution: {view_error}")
            raise

        end = datetime.datetime.now()
        duration = end - start
        path = request.path

        try:
            if path == "/v1/analyze/content/":
                if request.method == 'POST':
                    auth_header = request.headers.get('Authorization', '')
                    if auth_header.startswith('Bearer '):
                        api_key_raw = auth_header.split('Bearer ')[1]
                        key_obj = APIKey.objects.filter(
                            key_hash=api_key_raw).first()

                        if key_obj:
                            RequestLog.objects.create(
                                key=key_obj,
                                path=request.path,
                                method=request.method,
                                status_code=response.status_code,
                                ip_address=request.META.get("REMOTE_ADDR"),
                                duration=duration,
                            )
                else:
                    print('Middleware error')
        except Exception as middleware_error:
            print(f"🚨 Middleware logging error: {middleware_error}")

        return response