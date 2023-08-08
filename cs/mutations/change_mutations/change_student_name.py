import graphene

from order.models import OrderDetail


class ChangeStudentName(graphene.Mutation):
    class Arguments:
        order_detail_id = graphene.Int(required=True)
        changed_name = graphene.String(required=True)
        changing_name = graphene.String(required=True)

    success = graphene.Boolean(default_value=False, required=True)
    message = graphene.String(required=True)

    @classmethod
    def mutate(cls, _, __, order_detail_id, changed_name, changing_name):

        try:
            order_detail = OrderDetail.objects.get(pk=order_detail_id)
            order_detail.student_names.remove(changed_name)
            order_detail.student_names.append(changing_name)
            order_detail.save()
            return ChangeStudentName(success=True, message='학생이름이 변경되었습니다.')
        except Exception as e:
            print(e)
            return ChangeStudentName(message='학생이름 변경에 실패했습니다. 개발팀에게 문의해주세요.')

