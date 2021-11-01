from rest_framework import status
from rest_framework.response import Response


class CheckUserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'HTTP_USER_AGENT' in request.META:
            return response
        return Response('Request Should be Contain USERAGENT header', status=status.HTTP_400_BAD_REQUEST)
