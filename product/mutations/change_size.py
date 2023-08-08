import graphene

from product.models import ProductMaster


class ChangeSize(graphene.Mutation):
    class Arguments:
        product_master_id = graphene.Int()
        changed_size = graphene.String()
        changing_size = graphene.String()

    success = graphene.Boolean(default_value=False)
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, product_master_id, changed_size, changing_size):
        product_master = ProductMaster.objects.get(pk=product_master_id)
        if product_master.products.filter(size=changing_size).exists():
            return ChangeSize(success=False, message='이미 존재하는 사이즈입니다.')
        product_master.products.filter(size=changed_size).update(size=changing_size)
        return ChangeSize(success=True, message='사이즈가 변경되었습니다.')

