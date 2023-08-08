import graphene


class AuditionMasterInputType(graphene.InputObjectType):
    current_level = graphene.String()
    next_level = graphene.String()

