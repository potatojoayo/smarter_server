import graphene
from django.contrib.auth.hashers import check_password


class ChangePassword(graphene.Mutation):
    class Arguments:
        current_password = graphene.String()
        changing_password = graphene.String()

    success = graphene.Boolean()
    invalid = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, current_password, changing_password):
        user = info.context.user
        if not check_password(current_password, user.password):
            return ChangePassword(invalid=True, success=False)
        user.set_password(changing_password)
        user.save()
        return ChangePassword(success=True, invalid=False)
