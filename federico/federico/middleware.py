import logging

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure your logger with the name you will use in the LOGGING config
        self.logger = logging.getLogger('django.request')

    def __call__(self, request):
        response = self.get_response(request)
        # Attach the request method to the log record
        self.logger.info(f'Request to {request.path}', extra={'request_method': request.method})
        return response
