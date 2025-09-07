from django.http import HttpResponseForbidden

from .models import RequestLog
from .models import BlockedIP

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        path = request.path

        if self.is_ip_blocked(ip_address):
            return HttpResponseForbidden("Your IP has been blocked.")

        user = request.user if request.user.is_authenticated else None
        # Log the request
        RequestLog.objects.create(
            user=user,
            ip_address=ip_address, 
            path=path
            )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_ip_blocked(self, ip_address):
        return BlockedIP.objects.filter(ip_address=ip_address).exists()
    