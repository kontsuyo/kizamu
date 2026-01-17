from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from items import views

urlpatterns = [
    path("users/<str:username>/", views.UserProfileView.as_view(), name="user-profile"),
    path("items/<int:pk>/", views.ItemLogDetail.as_view(), name="itemlog-detail"),
    path("", views.ItemList.as_view(), name="item-list"),
    # path("<int:pk>/", views.ItemDetail.as_view(), name="item-detail"),
    path("logs/", views.ItemLogList.as_view(), name="itemlog-list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
