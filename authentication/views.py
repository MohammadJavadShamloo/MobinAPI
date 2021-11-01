import random
import secrets

from django.contrib.auth import get_user_model, authenticate
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Token
from .providers import Provider
from .serializers import RegistrationSerializer, LoginSerializer, SendOtpSerializer, ValidateOtpSerializer, \
    ChangePassSerializer, KillTokenSerializer


def find_provider(phone_number):
    for subclass in Provider.__subclasses__():
        if subclass.is_belong_to_provider(phone_number):
            return subclass
    else:
        return None


def send_code(phone_number):
    code = random.randint(1000, 9999)
    provider = find_provider(phone_number)
    provider.send_sms(phone_number, code)
    return code


def get_token(request):
    token_in_header = request.headers.get('USER-TOKEN', None)
    token = Token.objects.filter(key__exact=token_in_header)[0]
    return token


class RegistrationView(APIView):

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
                user_agent=request.META['HTTP_USER_AGENT'],
                user=user
            )
            token.save()
            data['Token Key'] = token.key
            data['Message'] = 'Registration Succeed.'
            data['error'] = serializer.errors
            return Response(data, status=status.HTTP_200_OK)
        data['Message'] = 'Registration Failed.'
        data['error'] = serializer.errors
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginView(APIView):

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
                    user_agent=request.META['HTTP_USER_AGENT'],
                    user=user
                )
                token.save()
                data['Token Key'] = token.key
                data['Message'] = 'Login Succeed'
                return Response(data, status=status.HTTP_200_OK)
            else:
                data['Message'] = 'Not Valid Credentials'
                data['error'] = serializer.errors
                return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            data['Message'] = 'Not Valid Credentials'
            data['error'] = serializer.errors
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)


class LogOutView(APIView):

    def delete(self, request):
        data = {}
        token = get_token(request)
        if not token:
            data['Message'] = 'There is No User With Given Token Or Invalid Token'
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        token.key = ''
        token.save()
        data['Message'] = 'User Logged Out.'
        return Response(data, status=status.HTTP_200_OK)


class SendOtpView(APIView):

    def get(self, request):
        data = {}
        serializer = SendOtpSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.filter(phone_number=serializer.data['phone_number'])[0]
            if not user:
                data['Message'] = 'User Not Found'
                data['error'] = serializer.errors
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            code = send_code(user.phone_number)
            cache.set(user.phone_number, code, 4 * 60)
            data['Message'] = 'Code Has Been Send For You'
            data['error'] = serializer.errors
            data['code'] = code
            return Response(data, status=status.HTTP_200_OK)
        data['Message'] = 'Not Valid Input'
        data['error'] = serializer.errors
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)


class ValidateOtpView(APIView):

    def get(self, request):
        data = {}
        serializer = ValidateOtpSerializer(data=request.data)
        token = get_token(request)
        if not token:
            data['Message'] = 'There is No User With Given Token Or Invalid Token'
            data['error'] = serializer.errors
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        user = token.user
        if serializer.is_valid():
            code = cache.get(user.phone_number, None)
            if serializer.data['otp_code'] == str(code):
                data['Message'] = 'Validation Succeed.'
                data['error'] = serializer.errors
                return Response(data, status=status.HTTP_200_OK)
            else:
                data['Message'] = 'Not Valid Otp Code Or Code Has Been Expired.'
                data['error'] = serializer.errors
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
        data['Message'] = 'Not Valid Otp Code'
        data['error'] = serializer.errors
        return Response(data, status.HTTP_406_NOT_ACCEPTABLE)


class ChangePassView(APIView):

    def patch(self, request):
        data = {}
        serializer = ChangePassSerializer(data=request.data)
        token = get_token(request)
        if not token:
            data['Message'] = 'There is No User With Given Token Or Invalid Token'
            data['error'] = serializer.errors
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        user = token.user
        if serializer.is_valid():
            if user.check_password(serializer.data['old_pass']):
                user.set_password(serializer.data['new_password1'])
                token.key = secrets.token_hex(38)
                token.save()
                data['Token Key'] = token.key
                data['Message'] = 'Password Has Been Set.'
                data['error'] = serializer.errors
                return Response(data, status=status.HTTP_200_OK)
            data['Message'] = 'Wrong Old Password'
            data['error'] = serializer.errors
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
        data['Message'] = 'Not Valid Otp Code'
        data['error'] = serializer.errors
        return Response(data, status.HTTP_406_NOT_ACCEPTABLE)


class ListTokensView(APIView):

    def get(self, request):
        data = {}
        token = get_token(request)
        if not token:
            data['Message'] = 'There is No User With Given Token Or Invalid Token'
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        user = token.user
        data['Message'] = 'Tokens Are Loaded'
        data.update({token.key: token.user_agent for token in user.tokens.all()})
        return Response(data, status=status.HTTP_200_OK)


class KillTokenView(APIView):

    def patch(self, request):
        data = {}
        serializer = KillTokenSerializer(data=request.data)
        token = get_token(request)
        if not token:
            data['Message'] = 'There is No User With Given Token Or Invalid Token'
            data['error'] = serializer.errors
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        user = token.user
        if serializer.is_valid():
            for token_key in serializer.data['list_of_tokens']:
                token = Token.objects.filter(key__exact=token_key['key'])[0]
                if user == token.user:
                    token.delete()
            data['Message'] = 'Your Belonging Tokens Are Deleted.'
            data['error'] = serializer.errors
            return Response(data, status=status.HTTP_200_OK)
        data['Message'] = 'Not Valid Token Keys'
        data['error'] = serializer.errors
        return Response(data, status.HTTP_406_NOT_ACCEPTABLE)