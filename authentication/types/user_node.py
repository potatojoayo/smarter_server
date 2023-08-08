import os

import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from business.types import GymType
from authentication.models import User
from base_classes import CountableConnectionBase
from business.types.gym.gym_node import GymNode


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)
        filter_fields = {
            'name': ['icontains'],
            'is_admin': ['exact'],
            'is_staff': ['exact'],
        }
        connection_class = CountableConnectionBase

    user_id = graphene.Int()
    gym = graphene.Field(GymType)
    gym_node = graphene.Field(GymNode)
    group = graphene.String()
    profile_image = graphene.String()

    @staticmethod
    def resolve_profile_image(root: User, _):
        if root.profile_image:
            return os.environ.get("BASE_URL")+root.profile_image.url
        return None

    @staticmethod
    def resolve_gym_node(root, _):
        return root.gym

    @staticmethod
    def resolve_user_id(root, _):
        return root.id

    @staticmethod
    def resolve_gyms(root, info):
        return root.gym

    @staticmethod
    def resolve_group(root, _):
        if root.groups.count() > 0:
            return root.groups.all().first().name
