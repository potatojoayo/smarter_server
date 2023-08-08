import graphene

from business.models import Gym, Agency


class UpdateUserInfo(graphene.Mutation):
    class Arguments:
        gym_id = graphene.Int()
        gym_name = graphene.String()
        user_name = graphene.String()
        phone = graphene.String()
        agency_name = graphene.String()
        memo = graphene.String()
        address = graphene.String()
        detail_address = graphene.String()
        zip_code = graphene.String()
        refund_account_bank = graphene.String()
        refund_account_no = graphene.String()
        refund_account_owner = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, gym_id, **kwargs):


        gym_name = kwargs.get('gym_name')
        user_name = kwargs.get('user_name')
        phone = kwargs.get('phone')
        agency_name = kwargs.get('agency_name')
        memo = kwargs.get('memo')
        address = kwargs.get('address')
        detail_address = kwargs.get('detail_address')
        zip_code = kwargs.get('zip_code')
        refund_account_bank = kwargs.get('refund_account_bank')
        refund_account_no = kwargs.get('refund_account_no')
        refund_account_owner = kwargs.get('refund_account_owner')
        try:
            gym = Gym.objects.get(pk=gym_id)
            user = gym.user
            if gym_name:
                gym.name = gym_name
            elif user_name:
                user.name = user_name
            elif phone:
                user.phone = phone
            elif agency_name:
                agency = Agency.objects.filter(name=agency_name).first()
                user.agency = agency
            elif memo:
                gym.memo = memo
            elif address:
                gym.address = address
                gym.detail_address = detail_address
                gym.zip_code = zip_code
            elif refund_account_bank:
                user.refund_account_bank = refund_account_bank
                user.refund_account_no = refund_account_no
                user.refund_account_owner = refund_account_owner
            gym.save()
            user.save()

            return UpdateUserInfo(success=True)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return UpdateUserInfo(success=False)
