from api.permissions import IsAdmin, IsAdminOrReadOnly, ReviewCommentPermission
from api.serializers import (
    CategorySerializer, CheckConfCodeSerializer,
    CommentSerializer, GenresSerializer,
    ReviewSerializer, SignupSerializer,
    TitleCreationSerializer, TitleSerializer,
    UserSerializer
)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from reviews.models import Category, Genres, Review, Title
from users.models import User

from api_yamdb.settings import DEFAULT_EMAIL


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


class TitleViewSet(ModelViewSet):
    """Title ViewSet."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year',)
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreationSerializer
        return self.serializer_class


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """Category ViewSet."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]


class GenresViewSet(CategoryViewSet):
    """Genres ViewSet."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Review ViewSet."""

    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Review Comment."""

    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)
