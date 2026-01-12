# pylint: disable=redefined-outer-name
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """未認証のAPIクライアント"""
    return APIClient()


@pytest.fixture
def test_user(db):
    """テスト用のユーザー作成"""
    _ = db  # Pylint/Pylance対策：参照されていることにする
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def auth_client(api_client, test_user):
    """認証済みのAPIクライアント"""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def other_user(db):
    """自分以外のユーザー"""
    _ = db  # Pylint/Pylance対策：参照されていることにする
    return get_user_model().objects.create_user(
        username="stranger", password="password123"
    )


@pytest.fixture
def other_auth_client(api_client, other_user):
    """自分以外のユーザーでログインしたクライアント"""
    api_client.force_authenticate(user=other_user)
    return api_client
