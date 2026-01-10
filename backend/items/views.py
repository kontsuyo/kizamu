from rest_framework import generics, permissions

from items.models import BootItem
from items.serializers import BootItemSerializer


class BootItemList(generics.ListCreateAPIView):
    queryset = BootItem.objects.all()
    serializer_class = BootItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BootItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BootItem.objects.all()
    serializer_class = BootItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
