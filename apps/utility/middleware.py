from __future__ import unicode_literals

class RequestIPV4Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipv4 = x_forwarded_for.split(',')[0]
        else:
            ipv4 = request.META.get('REMOTE_ADDR', None)
        request.ipv4 = ipv4

        response = self.get_response(request)

        return response
        