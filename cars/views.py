from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from cars.models import Brand, Model_auth, Car, Comment, Like
from cars.permission import IsAdminPermission, IsUserPermission
from cars.serializers import BrandSerializer, Model_authSerializer, CarListSerializer, CarSerializer, \
    CommentSerializer


class BrandListView(ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class Model_authListView(ListAPIView):
    queryset = Model_auth.objects.all()
    serializer_class = Model_authSerializer


class CarListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarListSerializer


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_url_kwarg = 'slug'
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['model_auth', 'brand', 'author']
    search_fields = ['title', 'author', 'brand__title', 'description']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return CarListSerializer
        return self.serializer_class


    @action(['GET'], detail=True)
    def comments(self, request, slug=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(['POST'], detail=True)
    def like(self, request, slug=None):
        car = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(car=car, user=user)
            like.is_liked = not like.is_liked
            like.save()
            message = 'liked' if like.is_liked else 'disliked'
        except Like.DoesNotExist:
            Like.objects.create(car=car, user=user, is_liked=True)
            message = 'liked'
        return Response(message, status=200)

    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsUserPermission]
        elif self.action == 'like':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cars': reverse('car-list', request=request, format=format),
        'brand': reverse('brand-list', request=request, format=format),
        'model_auth': reverse('model_auth-list', request=request, format=format),
    })


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.none()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

