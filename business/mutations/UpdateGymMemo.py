import graphene

from business.models import Gym


class UpdateGymMemo(graphene.Mutation):
    class Arguments:
        gym_id = graphene.Int(required=True)
        memo = graphene.String(required=True)

    success = graphene.Boolean(default_value=False)
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, gym_id, memo):
        try:
            gym = Gym.objects.get(pk=gym_id)
            gym.memo = memo
            gym.save()
            return UpdateGymMemo(success=True, message='체육관 메모가 성공적으로 저장되었습니다.')
        except Exception as e:
            print(e)
            return UpdateGymMemo(message='체육관 메모 저장에 실패했습니다. 개발팀에게 문의해주세요.')