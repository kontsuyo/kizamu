from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from accounts import views

urlpatterns = [
    path("users/", views.CustomUserList.as_view(), name="customuser-list"),
    path("users/<int:pk>/", views.CustomUserDetail.as_view(), name="customuser-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
