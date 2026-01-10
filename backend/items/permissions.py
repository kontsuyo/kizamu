from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    オブジェクトの所有者のみが編集を許可されるカスタム権限。
    """

    def has_object_permission(self, request, view, obj):
        # 読み取り権限はすべてのリクエストに許可され、
        # 常に GET、HEAD、または OPTIONS リクエストを許可します。
        if request.method in permissions.SAFE_METHODS:
            return True

        # アイテムの書き込み権限は、そのアイテムの所有者のみが許可されます。
        return obj.user == request.user
