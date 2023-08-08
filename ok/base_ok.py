import graphene


class BaseOk(graphene.Interface):
    ok_message = graphene.String(required=True)
