from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from items import views

urlpatterns = [
    path("boots/", views.BootItemList.as_view(), name="bootitem-list"),
    path("boots/<int:pk>/", views.BootItemDetail.as_view(), name="bootitem-detail"),
    path("logs/", views.BootLogList.as_view(), name="bootlog-list"),
    path("logs/<int:pk>/", views.BootLogDetail.as_view(), name="bootlog-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
