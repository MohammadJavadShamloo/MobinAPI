import time

from rest_framework import status
from rest_framework.response import Response

import logging

logger = logging.getLogger('middlelogger')


class CheckUserAgentMiddleware:
    """
    Check Agent User Middleware
    Checks every request whether has the HTTP_USER_AGENT header.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'HTTP_USER_AGENT' in request.META:
            return response
        return Response('Request Should be Contain USERAGENT header', status=status.HTTP_400_BAD_REQUEST)


class LoggerMiddleware:
    """
    Check Agent User Middleware
    Checks every request whether has the HTTP_USER_AGENT header.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        req_time = time.time()
        response = self.get_response(request)
        resp_time = time.time() - req_time
        logger.info('Middleware Log : ', extra={
            'path': str(request.path),
            'status_code': str(response.status_code),
            'run_time': round(resp_time * 10 ** 3, 3)
        })
        return response
