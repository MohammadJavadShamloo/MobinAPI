import secrets

from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Token
from .serializers import RegistrationSerializer, LoginSerializer


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
                login(request, user)
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
        token_in_header = request.headers.get('USER-TOKEN', None)
        print(token_in_header)
        print([token.key for token in Token.objects.all()])
        try:
            token = Token.objects.get(key=token_in_header)
        except Token.DoesNotExist:
            data['Message'] = 'There is No User With Given Token'
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        token.delete()
        data['Message'] = 'User Logged Out.'
        return Response(data, status=status.HTTP_200_OK)
