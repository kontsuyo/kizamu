from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response

from items.models import Item, Photo
from items.permissions import IsOwnerOrReadOnly
from items.serializers import (
    FeedSerializer,
    ItemCreateSerializer,
    ItemDetailSerializer,
    PhotoDetailSerializer,
    PhotoUploadSerializer,
    ProfileSerializer,
)


class Profile(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        username = self.kwargs.get("username")
        return get_user_model().objects.filter(username=username)


class ItemCreate(generics.CreateAPIView):
    serializer_class = ItemCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # 通常の保存処理
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # ユーザー名を追加してレスポンスを作成
        response_data = serializer.data
        response_data["username"] = request.user.username

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemDetailSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Item.objects.filter(pk=pk)


class PhotoUpload(generics.CreateAPIView):
    serializer_class = PhotoUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PhotoDetailSerializer
    permission_classes = (
        permissions.AllowAny,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Photo.objects.filter(pk=pk)


class FeedPagination(CursorPagination):
    page_size = 20
    ordering = "-created_at"


class Feed(generics.ListAPIView):
    """全ユーザーのフィード（投稿日時の新しい順）"""

    queryset = Photo.objects.filter(shared_feed=True).order_by("-created_at")
    serializer_class = FeedSerializer
    pagination_class = FeedPagination
