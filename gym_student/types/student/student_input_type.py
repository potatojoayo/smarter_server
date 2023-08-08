import graphene


class StudentInputType(graphene.InputObjectType):
    id = graphene.Int()
    class_name = graphene.String()
    level_name = graphene.String()
    school_name = graphene.String()
    name = graphene.String()
    birthday = graphene.Date()
    status = graphene.String()
    phone = graphene.String()
    height = graphene.Float()
    weight = graphene.Float()
    date_entered = graphene.Date()
    class_date_start = graphene.Date()
    day_to_pay = graphene.Int()
    gender = graphene.String()
    price_to_pay = graphene.Int()
    memo_for_health = graphene.String()
    memo_for_price = graphene.String()
    memo = graphene.String()
