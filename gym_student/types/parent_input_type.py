import graphene


class ParentInputType(graphene.InputObjectType):
    id = graphene.Int()
    phone = graphene.String()
    name = graphene.String()
    relationship_name = graphene.String()
    zip_code = graphene.String()
    address = graphene.String()
    detail_address = graphene.String()
    supporter_name = graphene.String()
    supporter_relationship = graphene.String()
    supporter_phone = graphene.String()
