import graphene

from product.models import ProductMaster


class ChangeColor(graphene.Mutation):
    class Arguments:
        product_master_id = graphene.Int()
        changed_color = graphene.String()
        changing_color = graphene.String()

    success = graphene.Boolean(default_value=False)
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, product_master_id, changed_color, changing_color):
        product_master = ProductMaster.objects.get(pk=product_master_id)
        if product_master.products.filter(color=changing_color).exists():
            return ChangeColor(success=False, message='이미 존재하는 색상입니다.')
        product_master.products.filter(color=changed_color).update(color=changing_color)
        return ChangeColor(success=True, message='색상이 변경되었습니다.')

