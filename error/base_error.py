import graphene


class BaseError(graphene.Interface):
    error_message = graphene.String(required=True)
