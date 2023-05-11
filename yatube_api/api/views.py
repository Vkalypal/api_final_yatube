from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from .permissions import IsAuthorOrReadOnly


from posts.models import Post, Group, Follow, User
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post

    def get_queryset(self):
        post = self.get_post()
        return post.comments

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = Follow.objects.filter(user=self.request.user)
        return user

    def perform_create(self, serializer):
        following = User.objects.get(username=self.request.data["following"])

        serializer.save(user=self.request.user, following=following)
