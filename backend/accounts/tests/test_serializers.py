import pytest
from accounts.serializers import UserRegisterSerializer


@pytest.mark.django_db
class TestUserRegisterSerializer:
    def test_create_user_success(self):
        """ユーザーが正常に作成される"""
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }
        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.username == "testuser"
        assert user.email == "testuser@example.com"
        assert user.check_password(
            "password123"
        )  # パスワードがハッシュ化されているか確認

    def test_passwords_do_not_match(self):
        """password と confirm_password が一致しない場合エラー"""
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "confirm_password": "123password",
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors
        assert serializer.errors["password"][0] == "Passwords do not match."  # pyright: ignore[reportCallIssue, reportArgumentType]
