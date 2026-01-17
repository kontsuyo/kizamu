from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format_=None, **kwargs):
    fmt = format_ if format_ is not None else kwargs.get("format")
    return Response(
        {
            "users": reverse("customuser-list", request=request, format=fmt),
            "boots": reverse("item-list", request=request, format=fmt),
        }
    )
