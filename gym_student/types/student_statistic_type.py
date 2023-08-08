import graphene


class StudentStatisticType(graphene.ObjectType):
    month = graphene.Int()
    total_student = graphene.Int()
    new_student = graphene.Int()
    out_student = graphene.Int()
