from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from items.models import BootItem


@pytest.mark.django_db
def test_str_returns_brand_and_model():
    user = get_user_model().objects.create_user(username="jdoe", password="pass")
    item = BootItem.objects.create(user=user, brand="Nike", model="Air", leather="full")
    assert str(item) == "Nike Air"


@pytest.mark.django_db
def test_ordering_by_created_at_desc():
    user = get_user_model().objects.create_user(username="jane", password="pass")
    now = timezone.now()
    older = BootItem.objects.create(
        user=user,
        brand="Brand1",
        model="Old",
        leather="x",
        created_at=now - timedelta(days=1),
    )
    newer = BootItem.objects.create(
        user=user,
        brand="Brand2",
        model="New",
        leather="y",
        created_at=now,
    )

    items = list(BootItem.objects.all())
    assert items[0] == newer
    assert items[1] == older


@pytest.mark.django_db
def test_related_name_boot_items():
    user = get_user_model().objects.create_user(username="alice", password="pass")
    item1 = BootItem.objects.create(user=user, brand="B1", model="M1", leather="l")
    item2 = BootItem.objects.create(user=user, brand="B2", model="M2", leather="l2")

    qs = user.boot_items.all()  # pyright: ignore[reportAttributeAccessIssue]
    assert qs.count() == 2
    assert item1 in qs and item2 in qs
