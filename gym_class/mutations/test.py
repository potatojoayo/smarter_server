import graphene
import datetime
class Test(graphene.Mutation):
    class Arguments:
        input = graphene.Date()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, input):
        now_date = datetime.date.today()
        print(now_date)
        print(type(now_date))
        print(input)
        print(type(input))
        print((input-now_date).days)
        print(type((input-now_date).days))
        return Test(success=True)
