import pytest
from django.db.utils import IntegrityError
from django.forms import ValidationError

from photo.models import Group, User, UserGroup
from photo.tests.factories import UserFactory


@pytest.mark.django_db
class TestGroup:
    def test_create_group(self):
        group = Group.objects.create(
            name="Test Group",
            description="A test group",
        )
        assert group.name == "Test Group"
        assert group.description == "A test group"
        assert group.created_at is not None

    def test_add_user_to_group(self):
        user = UserFactory()
        group = Group.objects.create(name="Test Group")
        user_group = UserGroup.objects.create(
            user=user,
            group=group,
            role="member",
        )
        assert user_group.user == user
        assert user_group.group == group
        assert user_group.role == "member"
        assert user_group.joined_at is not None

    def test_add_multiple_users_to_group(self):
        users = [UserFactory() for _ in range(3)]
        group = Group.objects.create(name="Test Group")

        for user in users:
            UserGroup.objects.create(
                user=user,
                group=group,
                role="member",
            )

        assert group.members.count() == 3
        for user in users:
            assert user in group.members.all()

    def test_user_cannot_join_group_twice(self):
        user = UserFactory()
        group = Group.objects.create(name="Test Group")
        UserGroup.objects.create(
            user=user,
            group=group,
            role="member",
        )

        with pytest.raises(IntegrityError):
            UserGroup.objects.create(
                user=user,
                group=group,
                role="admin",
            )

    def test_user_can_be_in_multiple_groups(self):
        user = UserFactory()
        group1 = Group.objects.create(name="Group 1")
        group2 = Group.objects.create(name="Group 2")

        UserGroup.objects.create(
            user=user,
            group=group1,
            role="member",
        )
        UserGroup.objects.create(
            user=user,
            group=group2,
            role="admin",
        )

        assert user.user_groups.count() == 2
        assert group1 in user.user_groups.all()
        assert group2 in user.user_groups.all()

    def test_soft_delete_group(self):
        group = Group.objects.create(name="Test Group")
        group.delete()
        assert group.is_deleted
        assert not Group.objects.filter(name="Test Group").exists()
        assert Group.all_objects.filter(name="Test Group").exists()

    def test_soft_delete_user_group(self):
        user = UserFactory()
        group = Group.objects.create(name="Test Group")
        user_group = UserGroup.objects.create(
            user=user,
            group=group,
            role="member",
        )
        user_group.delete()
        assert user_group.is_deleted
        assert not UserGroup.objects.filter(user=user, group=group).exists()
        assert UserGroup.all_objects.filter(user=user, group=group).exists()
