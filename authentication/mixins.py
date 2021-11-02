from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import Token


class AuthenticatedUsersMixin:

    def dispatch(self, request, *args, **kwargs):
        token_in_header = request.headers.get('USER-TOKEN')
        token = Token.objects.filter(key__exact=token_in_header)
        if token:
            self.token = token[0]
            self.user = self.token.user
        else:
            response = Response(status=status.HTTP_404_NOT_FOUND)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            return response
        self.check_user_agent(request)
        return super(AuthenticatedUsersMixin, self).dispatch(request, *args, **kwargs)

    def check_user_agent(self, request):
        if self.token.user_agent != request.META.get('HTTP_USER_AGENT'):
            self.token.user_agent = request.META.get('HTTP_USER_AGENT')
            self.token.save()