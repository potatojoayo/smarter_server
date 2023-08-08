import graphene

from authentication.models import User
from product.models import ProductMaster, Draft, Category, NewDraft


class DeleteMultipleDrafts(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        category_name = graphene.String()
        sub_category_name = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, user_id, category_name, sub_category_name):
        user = User.objects.get(pk=user_id)
        sub_category = Category.objects.get(parent__name=category_name,
                                        name=sub_category_name)
        NewDraft.objects.filter(user=user, sub_category=sub_category).update(is_delted=True)
        # product_masters = ProductMaster.objects.filter(category__name = category_name,
        #                                                sub_category__name = sub_category_name)
        # for product_master in product_masters:
        #     Draft.objects.filter(user=user, product_master=product_master).update(is_deleted=True)

        return DeleteMultipleDrafts(success=True)