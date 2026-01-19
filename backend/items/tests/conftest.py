import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from items.models import Item, Photo

User = get_user_model()


@pytest.fixture
def api_client():
    """未認証のAPIクライアント"""
    return APIClient()


@pytest.fixture
def test_user(db):
    """テスト用のユーザー作成"""
    _ = db
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def auth_client(api_client, test_user):
    """認証済みのAPIクライアント"""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def other_user(db):
    """自分以外のユーザー"""
    _ = db
    return User.objects.create_user(username="otheruser", password="password123")


@pytest.fixture
def other_auth_client(api_client, other_user):
    """他のユーザーの認証済みクライアント"""
    api_client.force_authenticate(user=other_user)
    return api_client


@pytest.fixture
def test_item(test_user):
    """テスト用のアイテム作成"""
    return Item.objects.create(
        user=test_user,
        _type="Footwear",
        brand="Nicks",
        model_name="TankerPro",
        leather="Waxed Flesh",
    )


@pytest.fixture
def test_photo(test_user, test_item):
    """テスト用の写真作成"""
    return Photo.objects.create(
        item=test_item,
        user=test_user,
        image="item_logs/test_image.jpg",
        note="テスト写真",
        wore_on="2025-01-19",
        shared_feed=True,
    )
