import pytest
from django.urls import reverse

from items.models import Item, Photo


@pytest.mark.django_db
class TestItemCreate:
    """ItemCreate エンドポイントのテスト"""

    def test_create_item_authenticated_user_success(self, auth_client, test_user):
        """認証ユーザーが正常にアイテムを作成できる"""
        data = {
            "_type": "Footwear",
            "brand": "DrMartens",
            "model_name": "1461",
            "leather": "smooth",
        }
        response = auth_client.post(reverse("item-create"), data)

        assert response.status_code == 201
        assert response.data["brand"] == "DrMartens"
        assert response.data["user"] == test_user.username

        # データベースに保存されているか確認
        item = Item.objects.get(brand="DrMartens")
        assert item.user == test_user
        assert item.model_name == "1461"

    def test_create_item_unauthenticated_user_forbidden(self, api_client):
        """未認証ユーザーはアイテム作成できない"""
        data = {
            "_type": "Footwear",
            "brand": "DrMartens",
            "model_name": "1461",
            "leather": "smooth",
        }
        response = api_client.post(reverse("item-create"), data)

        assert response.status_code == 403

    def test_create_item_missing_required_fields(self, auth_client):
        """必須フィールドがない場合エラー"""
        # brand が未指定
        data = {
            "_type": "Footwear",
            "model_name": "1461",
            "leather": "smooth",
        }
        response = auth_client.post(reverse("item-create"), data)

        assert response.status_code == 400
        assert "brand" in response.data

    def test_create_item_invalid_type_choice(self, auth_client):
        """無効な _type を指定するとエラー"""
        data = {
            "_type": "InvalidType",
            "brand": "DrMartens",
            "model_name": "1461",
            "leather": "smooth",
        }
        response = auth_client.post(reverse("item-create"), data)

        assert response.status_code == 400
        assert "_type" in response.data

    def test_create_item_user_is_automatically_set(self, auth_client, test_user):
        """user フィールドが自動的に設定される（指定不可）"""
        data = {
            "_type": "Footwear",
            "brand": "Nike",
            "model_name": "AirForce1",
            "leather": "canvas",
            # user を指定しても無視される
        }
        response = auth_client.post(reverse("item-create"), data)

        assert response.status_code == 201
        assert response.data["user"] == test_user.username


@pytest.mark.django_db
class TestItemDetail:
    """ItemDetail エンドポイントのテスト"""

    def test_retrieve_item_success(self, api_client, test_item):
        """アイテムを取得できる"""
        response = api_client.get(reverse("item-detail", kwargs={"pk": test_item.pk}))

        assert response.status_code == 200
        assert response.data["brand"] == "Nicks"
        assert response.data["model_name"] == "TankerPro"
        assert response.data["leather"] == "Waxed Flesh"

    def test_retrieve_item_not_found(self, api_client):
        """存在しないアイテムは404"""
        response = api_client.get(reverse("item-detail", kwargs={"pk": 9999}))

        assert response.status_code == 404

    def test_update_item_owner_success(self, auth_client, test_item):
        """所有者はアイテムを更新できる"""
        data = {
            "_type": "Footwear",
            "brand": "Nicks",
            "model_name": "TankerPro",
            "leather": "Chromexcel",  # 更新
        }
        response = auth_client.put(
            reverse("item-detail", kwargs={"pk": test_item.pk}), data
        )

        assert response.status_code == 200
        assert response.data["leather"] == "Chromexcel"

        # データベースで更新確認
        test_item.refresh_from_db()
        assert test_item.leather == "Chromexcel"

    def test_update_item_non_owner_forbidden(self, other_auth_client, test_item):
        """所有者以外は更新できない"""
        data = {
            "_type": "Footwear",
            "brand": "RedWing",
            "model_name": "Iron Ranger",
            "leather": "Leather",
        }
        response = other_auth_client.put(
            reverse("item-detail", kwargs={"pk": test_item.pk}), data
        )

        assert response.status_code == 403

    def test_delete_item_owner_success(self, auth_client, test_item):
        """所有者はアイテムを削除できる"""
        response = auth_client.delete(
            reverse("item-detail", kwargs={"pk": test_item.pk})
        )

        assert response.status_code == 204

        # データベースから削除確認
        assert not Item.objects.filter(pk=test_item.pk).exists()

    def test_delete_item_non_owner_forbidden(self, other_auth_client, test_item):
        """所有者以外は削除できない"""
        response = other_auth_client.delete(
            reverse("item-detail", kwargs={"pk": test_item.pk})
        )

        assert response.status_code == 403

        # データベースにまだ存在確認
        assert Item.objects.filter(pk=test_item.pk).exists()


@pytest.mark.django_db
class TestPhotoUpload:
    """PhotoUpload エンドポイントのテスト（MVP版：mockなし）"""

    def test_upload_photo_unauthenticated_user_forbidden(self, api_client, test_item):
        """未認証ユーザーは写真投稿できない"""
        data = {
            "item_id": test_item.pk,
            "note": "新しい靴",
            "wore_on": "2025-01-19",
            "shared_feed": True,
        }
        response = api_client.post(reverse("photo-upload"), data)

        assert response.status_code == 403

    def test_upload_photo_missing_required_fields(self, auth_client, test_item):
        """必須フィールド（image）がない場合エラー"""
        data = {
            "item_id": test_item.pk,
            "note": "新しい靴",
            "wore_on": "2025-01-19",
            "shared_feed": True,
        }
        response = auth_client.post(reverse("photo-upload"), data)

        assert response.status_code == 400
        assert "image" in response.data

    def test_upload_photo_invalid_item_id(self, auth_client):
        """存在しないitem_idでエラー"""
        data = {
            "item_id": 9999,
            "note": "新しい靴",
            "wore_on": "2025-01-19",
            "shared_feed": True,
        }
        response = auth_client.post(reverse("photo-upload"), data)

        assert response.status_code == 400


@pytest.mark.django_db
class TestPhotoDetail:
    """PhotoDetail エンドポイントのテスト（MVP版）"""

    def test_retrieve_photo_success(self, api_client, test_photo):
        """写真情報を取得できる"""
        response = api_client.get(reverse("photo-detail", kwargs={"pk": test_photo.pk}))

        assert response.status_code == 200
        assert response.data["note"] == "テスト写真"
        assert response.data["wore_on"] == "2025-01-19"

    def test_retrieve_photo_not_found(self, api_client):
        """存在しない写真は404"""
        response = api_client.get(reverse("photo-detail", kwargs={"pk": 9999}))

        assert response.status_code == 404


@pytest.mark.django_db
class TestPhotoEdit:
    """PhotoEdit エンドポイントのテスト（MVP版）"""

    def test_edit_photo_owner_success(self, auth_client, test_photo):
        """所有者は写真情報を編集できる"""
        data = {
            "note": "編集後のメモ",
            "wore_on": "2025-01-20",
            "shared_feed": False,
        }
        response = auth_client.patch(
            reverse("photo-edit", kwargs={"pk": test_photo.pk}), data
        )

        assert response.status_code == 200
        assert response.data["note"] == "編集後のメモ"

        # データベースで更新確認
        test_photo.refresh_from_db()
        assert test_photo.note == "編集後のメモ"
        assert test_photo.wore_on.strftime("%Y-%m-%d") == "2025-01-20"
        assert test_photo.shared_feed is False

    def test_edit_photo_non_owner_forbidden(self, other_auth_client, test_photo):
        """所有者以外は編集できない"""
        data = {
            "note": "不正な編集",
        }
        response = other_auth_client.patch(
            reverse("photo-edit", kwargs={"pk": test_photo.pk}), data
        )

        assert response.status_code == 403

    def test_edit_photo_unauthenticated_user_forbidden(self, api_client, test_photo):
        """未認証ユーザーは編集できない"""
        data = {
            "note": "不正な編集",
        }
        response = api_client.patch(
            reverse("photo-edit", kwargs={"pk": test_photo.pk}), data
        )

        assert response.status_code == 403

    def test_edit_photo_not_found(self, auth_client):
        """存在しない写真は404"""
        data = {
            "note": "編集",
        }
        response = auth_client.patch(reverse("photo-edit", kwargs={"pk": 9999}), data)

        assert response.status_code == 404

    def test_edit_photo_partial_update(self, auth_client, test_photo):
        """一部のフィールドのみ更新可能"""
        # noteだけ更新
        data = {
            "note": "メモだけ更新",
        }
        response = auth_client.patch(
            reverse("photo-edit", kwargs={"pk": test_photo.pk}), data
        )

        assert response.status_code == 200
        assert response.data["note"] == "メモだけ更新"

        # 他のフィールドは変更されていない
        test_photo.refresh_from_db()
        assert test_photo.wore_on.strftime("%Y-%m-%d") == "2025-01-19"
        assert test_photo.shared_feed is True


@pytest.mark.django_db
class TestPhotoDelete:
    """PhotoDestroy エンドポイントのテスト（MVP版）"""

    def test_delete_photo_owner_success(self, auth_client, test_photo):
        """所有者は写真を削除できる"""
        response = auth_client.delete(
            reverse("photo-delete", kwargs={"pk": test_photo.pk})
        )

        assert response.status_code == 204

        # データベースから削除確認
        assert not Photo.objects.filter(pk=test_photo.pk).exists()

    def test_delete_photo_non_owner_forbidden(self, other_auth_client, test_photo):
        """所有者以外は削除できない"""
        response = other_auth_client.delete(
            reverse("photo-delete", kwargs={"pk": test_photo.pk})
        )

        assert response.status_code == 403

        # データベースにまだ存在確認
        assert Photo.objects.filter(pk=test_photo.pk).exists()

    def test_delete_photo_unauthenticated_user_forbidden(self, api_client, test_photo):
        """未認証ユーザーは削除できない"""
        response = api_client.delete(
            reverse("photo-delete", kwargs={"pk": test_photo.pk})
        )

        assert response.status_code == 403

        # データベースにまだ存在確認
        assert Photo.objects.filter(pk=test_photo.pk).exists()

    def test_delete_photo_not_found(self, auth_client):
        """存在しない写真は404"""
        response = auth_client.delete(reverse("photo-delete", kwargs={"pk": 9999}))

        assert response.status_code == 404
