import graphene

from business.models import Gym


class CreateOrUpdateUserRefundAccount(graphene.Mutation):
    class Arguments:
        gym_id = graphene.Int()
        refund_account_bank = graphene.String()
        refund_account_no = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, gym_id, refund_account_bank, refund_account_no):
        try:
            gym = Gym.objects.get(pk=gym_id)
            user = gym.user
            user.refund_account_no = refund_account_no
            user.refund_account_bank = refund_account_bank
            user.save()

            return CreateOrUpdateUserRefundAccount(success=True)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CreateOrUpdateUserRefundAccount(success=False)