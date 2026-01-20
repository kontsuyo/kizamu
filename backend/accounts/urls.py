from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from accounts import views

urlpatterns = [
    path("list/", views.CustomUserList.as_view(), name="customuser-list"),
    path("<int:pk>/", views.CustomUserDetail.as_view(), name="customuser-detail"),
    path("register/", views.UserRegister.as_view(), name="user-register"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
