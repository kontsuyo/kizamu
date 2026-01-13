from rest_framework import generics, permissions, status
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        "フロントエンドでURLを組み立てなくて済むようにするため"
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            boot_item = BootItem.objects.get(pk=request.data["boot_item"])
            serializer = BootItemSerializer(boot_item, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return response
