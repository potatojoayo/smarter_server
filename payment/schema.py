
import graphene

from payment.mutations.cancel_payment import CancelPayment


class Query(graphene.ObjectType):
    temp_query = graphene.String()

class Mutation(graphene.ObjectType):
    cancel_payment = CancelPayment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
