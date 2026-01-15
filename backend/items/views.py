from rest_framework import generics, permissions, status
from rest_framework.response import Response

from items.models import Item, ItemLog
from items.permissions import IsOwnerOrReadOnly
from items.serializers import ItemLogSerializer, ItemSerializer


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )


class ItemLogList(generics.ListCreateAPIView):
    queryset = ItemLog.objects.all()
    serializer_class = ItemLogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        "フロントエンドでURLを組み立てなくて済むようにするため"
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            boot_item = Item.objects.get(pk=request.data["boot_item"])
            serializer = ItemSerializer(boot_item, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return response


class ItemLogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemLog.objects.all()
    serializer_class = ItemLogSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
