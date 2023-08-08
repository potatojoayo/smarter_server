import graphene


class AdditionalReceiveInputType(graphene.InputObjectType):
    id = graphene.Int()
    quantity_additional_received = graphene.Int()


    
