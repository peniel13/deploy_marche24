from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from datetime import datetime

ONLINE_TIMEOUT = 60  # secondes

class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            now = datetime.utcnow()
            cache.set(f'online-{request.user.id}', now, timeout=ONLINE_TIMEOUT)
