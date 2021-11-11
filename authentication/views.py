import json
import random
import secrets

import requests
from django.contrib.auth import get_user_model, authenticate
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .mixins import AuthenticatedUsersMixin
from .models import Token, ArchPic
from .providers import Provider
from .serializers import RegistrationSerializer, LoginSerializer, SendOtpSerializer, ValidateOtpSerializer, \
    ChangePassSerializer, KillTokenSerializer, ForgotPassSerializer, TokenSerializer, GetTimeSerializer, CodeSerializer

token_key_prefix = 'Token-Key'
error_key_prefix = 'Error'
code_prefix = 'Otp-Code'
http_user_agent_header = 'HTTP_USER_AGENT'

status_codes = {
    200: "Success",
    400: "Bad request",
    404: "Not found",
    403: "Forbidden",
}


def find_provider(phone_number):
    for subclass in Provider.__subclasses__():
        if subclass.is_belong_to_provider(phone_number):
            return subclass
    else:
        return None


def send_code(phone_number):
    code = random.randint(1000, 9999)
    provider = find_provider(phone_number)
    if provider:
        provider.send_sms(phone_number, code)
        return code
    else:
        return None


def get_response():
    return json.loads(requests.get("https://worldtimeapi.org/api/timezone/Asia/Tehran").text)


class RegistrationView(APIView):
    """
    Registration View
    Registering Users using POST method.
    """

    @swagger_auto_schema(
        query_serializer=RegistrationSerializer,
        responses={
            200: TokenSerializer(),
            404: status_codes[404],
        },
    )
    def post(self, request):
        data = {}
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.create_user(
                username=serializer.data['username'],
                phone_number=serializer.data['phone_number'],
            )
            user.set_password(serializer.data['password1'])
            user.save()
            token = Token.objects.create(
                key=secrets.token_hex(38),
                user_agent='Docker',
                user=user
            )
            token.save()
            data[token_key_prefix] = token.key
            data[error_key_prefix] = serializer.errors
            return Response(data, status=status.HTTP_200_OK)
        data[error_key_prefix] = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Login View
    Login Users using POST method.
    """

    @swagger_auto_schema(
        query_serializer=LoginSerializer(),
        responses={
            200: TokenSerializer(),
            403: status_codes[403],
            400: status_codes[400]
        },
    )
    def post(self, request):
        data = {}
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(request=request,
                                username=serializer.data['username'],
                                password=serializer.data['password'])
            if user:
                token = Token.objects.create(
                    key=secrets.token_hex(38),
                    user_agent='Docker',
                    user=user
                )
                token.save()
                data[token_key_prefix] = token.key
                return Response(data, status=status.HTTP_200_OK)
            else:
                data[error_key_prefix] = serializer.errors
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        data[error_key_prefix] = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(AuthenticatedUsersMixin, APIView):
    """
    Log Out View
    Log Out Users using DELETE method.
    """

    @swagger_auto_schema(
        responses={
            200: status_codes[200],
        },
    )
    def delete(self, request):
        data = {}
        token = self.token
        token.key = ''
        token.save()
        return Response(data, status=status.HTTP_200_OK)


class SendOtpView(APIView):
    """
    Send OTP View
    Send OTP to Users using GET method.
    """

    @swagger_auto_schema(
        query_serializer=SendOtpSerializer(),
        responses={"password1": "MohaJav1380@@",
                   200: CodeSerializer(),
                   400: status_codes[400],
                   404: status_codes[404]
                   },
    )
    def post(self, request):
        data = {}
        serializer = SendOtpSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.filter(phone_number=serializer.data['phone_number'])
            if not user:
                data[error_key_prefix] = serializer.errors
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            user = user[0]
            code = send_code(user.phone_number)
            if code:
                cache.set(user.phone_number, code, 4 * 60)
                data[error_key_prefix] = serializer.errors
                data[code_prefix] = code
                return Response(data, status=status.HTTP_200_OK)
        data[error_key_prefix] = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ValidateOtpView(AuthenticatedUsersMixin, APIView, ):
    """
    Validate OTP View
    Validate OTP using GET method.
    """

    @swagger_auto_schema(
        query_serializer=ValidateOtpSerializer(),
        responses={
            200: status_codes[200],
            403: status_codes[403],
            400: status_codes[400]
        },
    )
    def get(self, request):
        data = {}
        serializer = ValidateOtpSerializer(data=request.data)
        if serializer.is_valid():
            code = cache.get(self.user.phone_number, None)
            if serializer.data['otp_code'] == str(code):
                self.user.is_phone_confirmed = True
                self.user.save()
                data[error_key_prefix] = serializer.errors
                return Response(data, status=status.HTTP_200_OK)
            else:
                data[error_key_prefix] = serializer.errors
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data[error_key_prefix] = serializer.errors
        return Response(data, status.HTTP_400_BAD_REQUEST)


class ChangePassView(AuthenticatedUsersMixin, APIView):
    """
    Change Password View
    Changing Password of Users using PATCH method.
    """

    @swagger_auto_schema(
        query_serializer=ChangePassSerializer(),
        responses={
            200: TokenSerializer(),
            400: status_codes[400]
        },
    )
    def patch(self, request):
        data = {}
        serializer = ChangePassSerializer(data=request.data)
        if serializer.is_valid():
            if self.user.check_password(serializer.data['old_pass']):
                self.user.set_password(serializer.data['new_password1'])
                self.token.key = secrets.token_hex(38)
                self.token.save()
                data[token_key_prefix] = self.token.key
                data[error_key_prefix] = serializer.errors
                return Response(data, status=status.HTTP_200_OK)
            data[error_key_prefix] = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data[error_key_prefix] = serializer.errors
        return Response(data, status.HTTP_400_BAD_REQUEST)


class ListTokensView(AuthenticatedUsersMixin, APIView, ):
    """
    List Tokens View
    Listing All Tokens of Users using GET method.
    """

    @swagger_auto_schema(
        responses={
            200: TokenSerializer(many=True),
        },
    )
    def patch(self, request):
        data = {}
        data.update({token.key: token.user_agent for token in self.user.tokens.all()})
        return Response(data, status=status.HTTP_200_OK)


class KillTokenView(AuthenticatedUsersMixin, APIView, ):
    """
    Kill Tokens View
    Killing Selected Tokens of Users using PATCH method.
    """

    @swagger_auto_schema(
        request_body=TokenSerializer(many=True),
        responses={
            200: status_codes[200],
            400: status_codes[400]
        },
    )
    def patch(self, request):
        data = {}
        serializer = KillTokenSerializer(data=request.data)
        if serializer.is_valid():
            for token_key in serializer.data['list_of_tokens']:
                token = Token.objects.filter(key__exact=token_key['key'])
                if token:
                    token = token[0]
                    if self.user == token.user:
                        token.delete()
            data[error_key_prefix] = serializer.errors
            return Response(data, status=status.HTTP_200_OK)
        data[error_key_prefix] = serializer.errors
        return Response(data, status.HTTP_400_BAD_REQUEST)


class ForgotPassView(APIView):
    """
    Forgot Password View
    Change Forgotten Password of Users using PATCH method.
    """

    @swagger_auto_schema(
        query_serializer=ForgotPassSerializer(),
        responses={
            200: TokenSerializer(),
            403: status_codes[403],
            400: status_codes[400]
        },
    )
    def patch(self, request):
        data = {}
        serializer = ForgotPassSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.data['phone_number']
            user = get_user_model().objects.filter(phone_number=phone_number)
            if not user:
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            user = user[0]
            otp_code = cache.get(phone_number, None)
            if serializer.data['otp_code'] == str(otp_code):
                user.set_password(serializer.data['new_password1'])
                token = Token.objects.create(
                    key=secrets.token_hex(38),
                    user_agent='Docker',
                    user=user
                )
                token.save()
                user.save()
                data[token_key_prefix] = token.key
                data[error_key_prefix] = serializer.errors
                return Response(data, status=status.HTTP_200_OK)
            else:
                data[error_key_prefix] = serializer.errors
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        data[error_key_prefix] = serializer.errors
        return Response(data, status.HTTP_400_BAD_REQUEST)


class GetWorldTimeView(AuthenticatedUsersMixin, APIView):
    @swagger_auto_schema(responses={
        200: GetTimeSerializer(),
        400: status_codes[400]
    })
    def get(self, request):
        data = {}
        time_data = get_response()
        if time_data:
            data['day_of_week'] = time_data['day_of_week']
            data['timezone'] = time_data['timezone']
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ShowArchPicView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        picture = ArchPic.objects.last()
        deleted_picture = ArchPic.objects.first().delete() if ArchPic.objects.count() > 1 else None
        return render(request,
                      'admin/utils/archPicPage.html',
                      {'picture': picture})


class DeleteArchPicView(LoginRequiredMixin, DeleteView):
    model = ArchPic
    success_url = reverse_lazy('admin:index')


@method_decorator(csrf_exempt, name='dispatch')
class UpdateArchPicView(LoginRequiredMixin, UpdateView):
    model = ArchPic
    success_url = reverse_lazy('admin:index')
    fields = [
        'picture',
        'title',
    ]
    template_name = 'admin/utils/archUpdateCreate.html'


@method_decorator(csrf_exempt, name='dispatch')
class CreateArchPicView(LoginRequiredMixin, CreateView):
    model = ArchPic
    success_url = reverse_lazy('admin:index')
    fields = [
        'picture',
        'title',
    ]
    template_name = 'admin/utils/archUpdateCreate.html'
