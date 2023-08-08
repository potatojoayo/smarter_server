import graphene


class NewDraftInputType(graphene.InputObjectType):
    printing = graphene.String(default_value='없음')
    price_work = graphene.Int(required=True)
    price_work_labor = graphene.Int(required=True)
    memo = graphene.String(default_value='')
    font = graphene.String(default_value='없음')
    thread_color = graphene.String(default_value='없음')

    

