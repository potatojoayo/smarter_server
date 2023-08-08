import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import ProtectedError

from product.models import Category
from product.types.category.category_type import CategoryType
from product.types.category.category_input_type import CategoryInputType


class UpdateCategory(graphene.Mutation):
    class Arguments:
        updating_categories = graphene.List(CategoryInputType)
        deleting_category_ids = graphene.List(graphene.Int)

    categories = graphene.List(CategoryType)
    product_exists = graphene.Boolean(default_value=False)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, updating_categories, deleting_category_ids):
        for deleting_id in deleting_category_ids:
            category = Category.objects.get(pk=deleting_id)
            products = category.products
            sub_products = category.sub_products
            if products.all().count() > 0 or sub_products.all().count() > 0:
                return UpdateCategory(product_exists=True)
            else:
                category.delete()
        for updating_category in updating_categories:
            # 새로 만드는 경우
            if updating_category.id < 0:

                # parent값이 있는 경우 없는 경우 구분, 하위카테고리(children)이 있는지 없는지 체크
                # parent값이 없는 걸로 하위카테고리 설정

                category = Category.objects.create(name=updating_category.name, order=updating_category.order, depth=updating_category.depth)

                # 하위카테고리에 접근
                for child in updating_category.children:
                    if child.id < 0:
                        Category.objects.create(name=child.name, order=child.order, depth=child.depth, parent_id=category.id)
                    else:
                        old_child = Category.objects.get(pk=child.id)
                        old_child.name = child.name
                        old_child.order = child.order
                        old_child.depth = child.depth
                        old_child.parent_id = category.id
                        old_child.save()

            # 업데이트 하는 경우

            else:
                category = Category.objects.get(pk=updating_category.id)
                category.name = updating_category.name
                category.order = updating_category.order
                category.depth = updating_category.depth
                category.parent_id = updating_category.parent
                category.save()
                for child in updating_category.children:
                    if child.id < 0:
                        Category.objects.create(name=child.name, order=child.order, depth=child.depth, parent_id=category.id)
                    else:
                        old_child = Category.objects.get(pk=child.id)
                        old_child.name = child.name
                        old_child.order = child.order
                        old_child.depth = child.depth
                        old_child.parent_id = category.id
                        old_child.save()

        return UpdateCategory(categories=Category.objects.filter(depth=0))







