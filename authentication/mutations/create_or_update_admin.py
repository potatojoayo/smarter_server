import graphene
from django.contrib.auth.models import Group, Permission
from django.db import IntegrityError, transaction

from authentication.models import User
from authentication.types.user_input_type import UserInputType


class CreateOrUpdateAdmin(graphene.Mutation):
    class Arguments:
        user = UserInputType()
        group = graphene.String()

    success = graphene.Boolean()
    duplicated = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, user, group):
        if user.id:
            User.objects.filter(pk=user.id).update(**user)
            new_user = User.objects.get(pk=user.id)
            if user.password:
                new_user.set_password(user.password)
                new_user.save()
        else:
            try:
                new_user = User.objects.create_superuser(**user)
            except IntegrityError:
                return CreateOrUpdateAdmin(success=False, duplicated=True)

        if group:
            new_group, created = Group.objects.get_or_create(name=group)
            if created:
                permissions = Permission.objects.all()
                for p in permissions:
                    new_group.permissions.add(p)
            try:
                old_group = new_user.groups.all().first()
                old_group.user_set.remove(new_user)
            except:
                pass
            new_group.user_set.add(new_user)

        return CreateOrUpdateAdmin(success=True, duplicated=False)
