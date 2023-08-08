import graphene

from gym_student.models import Student
from gym_student.types.student.student_input_type import StudentInputType


class UpdateStudents(graphene.Mutation):
    class Arguments:
        students = graphene.List(StudentInputType)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, students):
        for s in students:
            student = Student.objects.get(pk=s.id)
            student.name = s.name
            student.gender = s.gender
            student.birthday = s.birthday
            student.phone = s.phone
            student.school.name = s.school_name
            student.school.save()
            student.height = s.height
            student.weight = s.weight
            print(student)
            student.save()

        return UpdateStudents(success=True)
