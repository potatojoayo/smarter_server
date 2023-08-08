import graphene

from gym_student.models import Parent, School
from gym_student.types.student.student_input_type import StudentInputType


class UpdateStudent(graphene.Mutation):
    class Arguments:
        student_lists = graphene.List(StudentInputType)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, student_lists):
        user = info.context.user
        parent = Parent.objects.get(user=user)
        students = parent.students.all()
        for student in students:
            for student_list in student_lists:
                if student.id == student_list.id:
                    student.name = student_list.name
                    student.birthday = student_list.birthday
                    student.height = student_list.height
                    student.weight = student_list.weight
                    school = School.objects.get(pk=student_list.school_id)
                    student.school = school
                    student.phone = student_list.phone
                    student.save()
        return UpdateStudent(success=True)

