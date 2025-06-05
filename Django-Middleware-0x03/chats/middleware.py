import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Configure file-based logger
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        path = request.path
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.logger.info(f"{timestamp} - User: {user} - Path: {path}")

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        restricted_path = '/chats/'

        # Block access if not between 18 (6PM) and 21 (9PM)
        if request.path.startswith(restricted_path) and not (18 <= current_hour < 21):
            return HttpResponseForbidden("Access to chats is only allowed between 6PM and 9PM.")

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_limits = {}

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if request.method == 'POST':
            current_time = timezone.now()

            if ip in self.message_limits:
                last_request_time, count = self.message_limits[ip]
                time_diff = current_time - last_request_time

                if time_diff.total_seconds() > 60:
                    self.message_limits[ip] = (current_time, 1)
                else:
                    if count >= 5:
                        return HttpResponseForbidden("You have exceeded the message limit. Please try again later.")
                    else:
                        self.message_limits[ip] = (current_time, count + 1)
            else:
                self.message_limits[ip] = (current_time, 1)

        response = self.get_response(request)
        return response

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not (request.user.is_superuser or request.user.groups.filter(name='moderator').exists()):
                return HttpResponseForbidden("You do not have permission to access this resource.")
        else:
            return HttpResponseForbidden("You are not authenticated.")

        response = self.get_response(request)
        return response