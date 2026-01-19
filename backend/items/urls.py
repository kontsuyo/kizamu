from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from items import views

urlpatterns = [
    path("", views.Feed.as_view(), name="feed"),
    path("users/<str:username>/", views.Profile.as_view(), name="profile"),
    path("items/create/", views.ItemCreate.as_view(), name="item-create"),
    path("items/<int:pk>/", views.ItemDetail.as_view(), name="item-detail"),
    path("photos/upload/", views.PhotoUpload.as_view(), name="photo-upload"),
    path("photos/<int:pk>/", views.PhotoDetail.as_view(), name="photo-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
