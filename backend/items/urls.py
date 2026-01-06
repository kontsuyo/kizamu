from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from items import views

urlpatterns = [
    path("items/boots/", views.BootItemList.as_view(), name="bootitem-list"),
    path("items/boots/<int:pk>/", views.BootItemDetail.as_view(), name="bootitem-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
