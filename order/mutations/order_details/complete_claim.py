import graphene

from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from order.models import Claim


class CompleteClaim(graphene.Mutation):
    class Arguments:
        claim_ids = graphene.List(graphene.Int)
        refund_price = graphene.Int()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, **kwargs):
        claim_ids = kwargs.get('claim_ids')
        refund_price = kwargs.get('refund_price')
        for claim_id in claim_ids:
            claim = Claim.objects.get(pk=claim_id)
            product = claim.order_detail.product
            quantity = claim.quantity
            user = claim.user
            if claim.state == "교환요청":
                state = '교환완료'
                Claim.objects.filter(pk=claim.id).update(state=state)
                #send_notification(user=user, type="교환완료", product_names=product.name, quantity=quantity)
            else:
                state = '반품완료'
                Claim.objects.filter(pk=claim.id).update(state=state, refund_price=refund_price)
                gym = claim.user.gym
                gym.total_purchased_amount -= claim.price_products + claim.price_total_work
                gym.save()
                #send_notification(user=user, type="반품완료", product_names=product.name, quantity=quantity)


        return CompleteClaim(success=True)



