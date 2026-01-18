from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from items.models import Item, Photo
from items.permissions import IsOwnerOrReadOnly
from items.serializers import (
    ItemCreateSerializer,
    ItemDetailSerializer,
    PhotoDestroySerializer,
    PhotoDetailSerializer,
    PhotoEditSerializer,
    PhotoUploadSerializer,
    ProfileSerializer,
)


class PhotoUpload(generics.CreateAPIView):
    serializer_class = PhotoUploadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PhotoDetail(generics.RetrieveAPIView):
    serializer_class = PhotoDetailSerializer
    permission_classes = (
        permissions.AllowAny,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Photo.objects.filter(pk=pk)


class PhotoEdit(generics.UpdateAPIView):
    serializer_class = PhotoEditSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Photo.objects.filter(pk=pk)


class PhotoDelete(generics.DestroyAPIView):
    serializer_class = PhotoDestroySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Photo.objects.filter(pk=pk)


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


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemDetailSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Item.objects.filter(pk=pk)
