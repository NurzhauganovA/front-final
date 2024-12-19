from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

from .models import User
from .serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer, UserCheckResetCodeSerializer, \
    UserResetPasswordSerializer, UserSerializer, SendResetPasswordCodeSerializer
from .utils import *


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(tags=["user settings"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        tags=["user settings"],
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('last_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('phone', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('iin', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('id_card_image', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
        ]
    )
    def post(self, request, *args, **kwargs):
        send_activation_code('verify_email', request.data.get('email'))

        return super().post(request, *args, **kwargs)


class UserVerifyEmailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCheckResetCodeSerializer

    @swagger_auto_schema(tags=["user settings"])
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        email = request.user.email
        if check_activation_code('verify_email', email, code):
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            return Response({'message': 'Email успешно подтвержден'})


class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    @swagger_auto_schema(tags=["user settings"])
    def post(self, request, *args, **kwargs):
        user = request.user
        user.auth_token.delete()
        return Response({'message': 'Пользователь успешно вышел из системы'})


class SendResetPasswordCodeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendResetPasswordCodeSerializer

    @swagger_auto_schema(tags=["user settings"])
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        send_activation_code('reset_password', email)
        return Response({'message': f'Код для сброса пароля отправлен на {email}'})


class CheckResetPasswordCodeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCheckResetCodeSerializer

    @swagger_auto_schema(tags=["user settings"])
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = int(request.data.get('code'))
        if check_activation_code('reset_password', email, code):
            return Response({'message': 'Код верный'})
        return Response({'message': 'Введен неверный код'}, status=400)


class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserResetPasswordSerializer

    @swagger_auto_schema(tags=["user settings"])
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('password_confirm')

        if password != confirm_password:
            return Response({'error': 'Пароли не совпадают'}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'Пользователь не найден'}, status=404)

        user.set_password(password)
        user.save()

        return Response({'message': 'Пароль успешно изменен'})


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(tags=["user settings"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
