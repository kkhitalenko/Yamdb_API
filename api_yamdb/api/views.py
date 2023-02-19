from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from api.serializers import (
    CheckConfCodeSerializer, SignupSerializer, UserSerializer
)
from api.permissions import IsAdmin
from api_yamdb.settings import DEFAULT_EMAIL
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')


class UserPersonalPageView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, data=request.data,)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, data=request.data, partial=True,)
        if serializer.is_valid():
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST,
        )


class SignupView(CreateAPIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        user = User.objects.get_or_create(username=request.data['username'])
        email = request.data['email']
        conf_code = default_token_generator.make_token(user)
        user.conf_code = conf_code
        # user.save()
        send_mail(
            subject='Код подтверждения',
            message=f'confirmation_code:{conf_code}',
            from_email=DEFAULT_EMAIL,
            recipient_list=[email, ],
        )
        return Response(
            f'Код подтверждения отправлен на адрес {email}',
            status=status.HTTP_200_OK,
        )


class GetTokenView(CreateAPIView):
    def post(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = CheckConfCodeSerializer(data=request.data)
        if serializer.is_valid():
            # user = get_object_or_404(
            #     User, username=serializer.validated_data['username']
            # )
            if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']
            ):
                return Response('Успешно', status.HTTP_200_OK,)
            return Response('Неверный код', status.HTTP_400_BAD_REQUEST,)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,)
