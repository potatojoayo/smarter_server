import graphene

from product.models import ProductMaster


class UpdateProductMasterMemo(graphene.Mutation):
    class Arguments:
        product_master_id = graphene.Int()
        memo = graphene.String()

    success = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, _, __, product_master_id, memo):
        try:
            ProductMaster.objects.filter(pk=product_master_id).update(memo=memo)
            return UpdateProductMasterMemo(success=True)
        except Exception as e:
            print(e)
            return UpdateProductMasterMemo()
