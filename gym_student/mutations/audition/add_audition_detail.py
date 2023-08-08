import graphene

from gym_student.models import AuditionMaster, Student, AuditionDetail


class AddAuditionDetail(graphene.Mutation):
    class Arguments:
        audition_master_id = graphene.Int()
        student_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, audition_master_id, student_ids):
        audition_master = AuditionMaster.objects.get(pk=audition_master_id)
        students = Student.objects.filter(pk__in=student_ids)
        for student in students:
            AuditionDetail.objects.create(audition_master=audition_master,
                                          student=student)

        return AddAuditionDetail(success=True)