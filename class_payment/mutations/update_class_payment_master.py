import graphene

from class_payment.models import ClassPaymentMaster


class UpdateClassPaymentMaster(graphene.Mutation):
    class Arguments:
        class_payment_id = graphene.Int()
        price = graphene.Int()
        memo = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, class_payment_id, **kwargs):
        class_payment_master = ClassPaymentMaster.objects.get(pk=class_payment_id)
        if 'price' in kwargs:
            price = kwargs.get('price')
            class_payment_master.price_to_pay = price
        if 'memo' in kwargs:
            memo = kwargs.get('memo')
            class_payment_master.memo = memo
        class_payment_master.save()
        return UpdateClassPaymentMaster(success=True)
