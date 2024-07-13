from django.contrib import auth
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework import exceptions
from .serializers import PrivateUserSerializer, TinyUserSerializer
from .models import User

import jwt


class Me(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_user = serializer.save()
            return Response(PrivateUserSerializer(updated_user).data)
        else:
            return Response(serializer.errors)


class Users(APIView):

    def post(self, request):
        password = request.data["password"]
        if not password:
            raise exceptions.ParseError

        serializer = PrivateUserSerializer(data=request.data)
        # ModelSerializer의 validation은 uniqueness도 자동으로 해준다.
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(password)
            new_user.save()
            return Response(PrivateUserSerializer(new_user).data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound

        serializer = TinyUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            raise exceptions.ParseError("ParseError")

        # 장고의 매직! check_passwrod와 set_password
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError("ParseError")

        # django의 authenticate함수는 정보가 맞으면 user를 리턴하고, 안 맞으면 None을 리턴
        user = auth.authenticate(request, username=username, password=password)

        if user:
            # django의 로그인 function으로 아주 쉽게 할 수 있다
            auth.login(request, user)
            return Response({"ok": "True"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogOut(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        auth.logout(request)
        return Response({"ok": "Bye"})


class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError("ParseError")

        user = auth.authenticate(request, username=username, password=password)

        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
