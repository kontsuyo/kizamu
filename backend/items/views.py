from rest_framework import generics, permissions

from items.models import BootItem, BootLog
from items.permissions import IsOwnerOrReadOnly
from items.serializers import BootItemSerializer, BootLogSerializer


class BootItemList(generics.ListCreateAPIView):
    queryset = BootItem.objects.all()
    serializer_class = BootItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BootItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BootItem.objects.all()
    serializer_class = BootItemSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )


class BootLogList(generics.ListCreateAPIView):
    queryset = BootLog.objects.all()
    serializer_class = BootLogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
