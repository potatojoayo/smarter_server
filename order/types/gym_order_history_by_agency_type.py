import graphene


class GymOrderHistoryByAgencyType(graphene.ObjectType):

    gym_name = graphene.String()
    agency_name = graphene.String()
    user_name = graphene.String()
    date_created = graphene.Date()
    product_name = graphene.String()
    price_gym = graphene.Int()
    quantity =graphene.Int()
    price_total = graphene.Int()
