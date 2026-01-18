from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from items import views

urlpatterns = [
    path("users/<str:username>/", views.Profile.as_view(), name="profile"),
    path("items/create/", views.ItemCreate.as_view(), name="item-create"),
    path("items/<int:pk>/", views.ItemDetail.as_view(), name="item-detail"),
    path("photos/upload/", views.PhotoUpload.as_view(), name="photo-upload"),
    path("photos/<int:pk>/", views.PhotoDetail.as_view(), name="photo-detail"),
    path("photos/edit/<int:pk>/", views.PhotoEdit.as_view(), name="photo-edit"),
    path("photos/delete/<int:pk>/", views.PhotoDelete.as_view(), name="photo-delete"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
