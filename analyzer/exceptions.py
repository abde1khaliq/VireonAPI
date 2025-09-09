from rest_framework.exceptions import APIException

class RateLimitExceeded(APIException):
    status_code = 429
    default_detail = "Rate limit exceeded. Try again later."
    default_code = "rate_limit_exceeded"
