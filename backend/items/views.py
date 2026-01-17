from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from items.models import Item, ItemLog
from items.serializers import (
    ItemCreateSerializer,
    ItemDetailSerializer,
    ItemListSerializer,
    ItemLogSerializer,
)

# class ItemLogList(generics.ListCreateAPIView):
#     serializer_class = ItemLogSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#         return ItemLog.objects.filter(item_id=pk).order_by("-created_at")

#     def perform_create(self, serializer):
#         pk = self.kwargs.get("pk")
#         item = get_object_or_404(Item, pk=pk)
#         serializer.save(user=self.request.user, item=item)

#     def create(self, request, *args, **kwargs):
#         "フロントエンドでURLを組み立てなくて済むようにするため"
#         response = super().create(request, *args, **kwargs)
#         if response.status_code == status.HTTP_201_CREATED:
#             item = Item.objects.get(pk=request.data["item"])
#             serializer = ItemSerializer(item, context={"request": request})
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return response


class ItemLogDetail(generics.RetrieveAPIView):
    serializer_class = ItemLogSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return ItemLog.objects.filter(pk=pk)


class ItemList(generics.ListAPIView):
    serializer_class = ItemListSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        username = self.kwargs.get("username")
        return get_user_model().objects.filter(username=username)


class ItemDetail(generics.RetrieveAPIView):
    serializer_class = ItemDetailSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Item.objects.filter(pk=pk)


class ItemCreate(generics.CreateAPIView):
    serializer_class = ItemCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
