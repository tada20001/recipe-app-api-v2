# myapp/middleware.py
from django.http import HttpResponseForbidden
import ipaddress


class IPRangeMiddleware:
    """ # 192.168.1.x 범위를 허용"""
    ALLOWED_RANGES = [
        ipaddress.ip_network('192.168.1.0/24')
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        if client_ip:
            ip = ipaddress.ip_address(client_ip)
            if not any(ip in network for network in self.ALLOWED_RANGES):
                return HttpResponseForbidden("Forbidden")
        return self.get_response(request)
