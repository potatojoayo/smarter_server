from gym_student.types.student.student_type import StudentType
from graphene import relay


class StudentConnection(relay.Connection):
    class Meta:
        node = StudentType
