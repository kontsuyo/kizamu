from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from items import views

urlpatterns = [
    path("users/<str:username>/", views.Profile.as_view(), name="item-list"),
    path(
        "items/<int:pk>/",
        views.ItemDetail.as_view(),
        name="item-detail",
    ),
    path(
        "photos/<int:pk>/",
        views.PhotoDetail.as_view(),
        name="itemlog-detail",
    ),
    path("items/create/", views.ItemCreate.as_view(), name="item-create"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
