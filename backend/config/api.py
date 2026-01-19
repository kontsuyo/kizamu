from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format_=None, **kwargs):
    """APIルートエンドポイント - MVPに必要な最小限のエンドポイント一覧"""
    fmt = format_ if format_ is not None else kwargs.get("format")
    return Response(
        {
            # ユーザー関連
            "users": reverse("customuser-list", request=request, format=fmt),
            # プロフィール
            "profile": reverse(
                "profile", kwargs={"username": "USERNAME"}, request=request, format=fmt
            ),
            # アイテム（ブーツ）
            "items-create": reverse("item-create", request=request, format=fmt),
            "item-detail": reverse(
                "item-detail", kwargs={"pk": 1}, request=request, format=fmt
            ),
            # 写真投稿
            "photos-upload": reverse("photo-upload", request=request, format=fmt),
            "photo-detail": reverse(
                "photo-detail", kwargs={"pk": 1}, request=request, format=fmt
            ),
            # フィード
            "feed": reverse("feed", request=request, format=fmt),
        }
    )
