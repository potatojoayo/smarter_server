import graphene
from graphene_django import DjangoObjectType

from product.models import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

    children = graphene.List(lambda:CategoryType)
    id = graphene.Int()

    @staticmethod
    def resolve_id(root, _):
        return root.id

    @staticmethod
    def resolve_children(root,info,**kwargs):
        return root.children.all()


