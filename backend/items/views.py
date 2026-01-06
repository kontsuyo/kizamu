from rest_framework import generics

from items.models import BootItem
from items.serializers import BootItemSerializer


class BootItemList(generics.ListCreateAPIView):
    queryset = BootItem.objects.all()
    serializer_class = BootItemSerializer


class BootItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BootItem.objects.all()
    serializer_class = BootItemSerializer
