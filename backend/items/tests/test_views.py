import pytest
from django.urls import reverse
from rest_framework import status

from items.models import BootItem, BootLog


@pytest.mark.django_db
class TestBootItemAPI:
    URL = reverse("bootitem-list")

    def test_create_boot_item_happy_path(self, auth_client, test_user):
        """
        【ハッピーパス】
        ログインユーザーがデータをPOSTした際、
        1. 201 Createdが返ること
        2. DBに保存されたデータのuserが実行ユーザーと一致すること
        """
        data = {"brand": "Red Wing", "model": "875", "leather": "Oro Legacy"}

        response = auth_client.post(self.URL, data, format="json")

        # 1. ステータスコードの確認
        assert response.status_code == status.HTTP_201_CREATED

        # 2. データの整合性確認
        assert response.data["brand"] == "Red Wing"

        # 3. perform_createの検証 (userが自動セットされているか)
        boot = BootItem.objects.get(id=response.data["id"])
        assert boot.user == test_user

    def test_list_boot_items_happy_path(self, api_client, test_user):
        """
        【ハッピーパス】
        全ユーザー（未ログイン含む）がブーツ一覧を取得できること
        """
        # 事前にデータを作成しておく
        BootItem.objects.create(
            user=test_user, brand="Alden", model="Indy", leather="Chromexcel"
        )

        response = api_client.get(self.URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["brand"] == "Alden"


@pytest.mark.django_db
def test_update_boot_item_by_non_owner_fails(other_auth_client, test_user):
    boot = BootItem.objects.create(
        user=test_user, brand="Red Wing", model="875", leather="Oro"
    )
    url = reverse("bootitem-detail", kwargs={"pk": boot.pk})

    data = {"brand": "Hack Brand"}
    response = other_auth_client.put(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    boot.refresh_from_db()
    assert boot.brand == "Red Wing"


@pytest.mark.django_db
def test_create_boot_log_happy_path(auth_client, test_user):
    """【ハッピーパス】特定のブーツに対してログを投稿できるか"""
    boot = BootItem.objects.create(user=test_user, brand="Red Wing", model="875")
    url = reverse("bootlog-list")

    data = {"boot_item": boot.id, "note": "今日はオイルアップをしました。"}
    response = auth_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["note"] == "今日はオイルアップをしました。"
    assert response.data["boot_item"] == boot.id


@pytest.mark.django_db
def test_boot_item_detail_contains_logs(auth_client, test_user):
    """【ハッピーパス】ブーツ詳細APIに紐づくログが含まれているか"""
    boot = BootItem.objects.create(user=test_user, brand="Red Wing", model="875")
    BootLog.objects.create(boot_item=boot, user=test_user, note="ログ1")
    BootLog.objects.create(boot_item=boot, user=test_user, note="ログ2")

    url = reverse("bootitem-detail", kwargs={"pk": boot.pk})

    response = auth_client.get(url)
    print(response.data)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["logs"]) == 2
    assert response.data["logs"][0]["note"] == "ログ1"


@pytest.mark.django_db
def test_create_log_returns_parent_boot_item(auth_client, test_user):
    boot = BootItem.objects.create(user=test_user, brand="Red Wing", model="875")
    url = reverse("bootlog-list")

    data = {"boot_item": boot.id, "note": "メンテナンス完了"}
    response = auth_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    # レスポンスのトップレベルに "logs" が含まれている（＝BootItemのデータが返っている）か確認
    assert "logs" in response.data
    assert response.data["logs"][0]["note"] == "メンテナンス完了"
