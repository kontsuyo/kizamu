from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from items.models import Item, ItemLog
from items.permissions import IsOwnerOrReadOnly
from items.serializers import ItemLogSerializer, ItemSerializer, UserProfileSerializer


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
            item = Item.objects.get(pk=request.data["item"])
            serializer = ItemSerializer(item, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return response


class ItemLogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItemLog.objects.all()
    serializer_class = ItemLogSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )


class UserProfileView(generics.ListAPIView):
    queryset = ItemLog.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        username = self.kwargs.get("username")
        User = get_user_model()

        try:
            user = User.objects.get(username=username)
            return ItemLog.objects.filter(user=user)
        except User.DoesNotExist:
            return ItemLog.objects.none()
