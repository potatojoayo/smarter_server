import graphene

from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from order.models import Claim


class DeclineClaim(graphene.Mutation):
    class Arguments:
        claim_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, claim_ids):
        for claim_id in claim_ids:
            claim = Claim.objects.get(pk=claim_id)
            user = claim.user
            product_name = claim.order_detail.product.name
            quantity = claim.quantity
            if claim.state == "교환요청":
                #action = '교환'
                state = '교환반려'
                Claim.objects.filter(pk=claim.id).update(state=state)
                #send_notification(user=user, product_names=product_name, quantity=quantity, type="교환반려")
            else:
                #action = '반품'
                state = '반품반려'
                Claim.objects.filter(pk=claim.id).update(state=state)
                #send_notification(user=user, product_names=product_name, quantity=quantity, type="반품반려")

        return DeclineClaim(success=True)


