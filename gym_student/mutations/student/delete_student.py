from datetime import datetime

import graphene

from class_payment.models import ClassPaymentMaster
from gym_class.models import AttendanceMaster
from gym_student.models import Student


class DeleteStudent(graphene.Mutation):
    class Arguments:
        student_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, student_id):
        today = datetime.today()
        now = datetime.now()
        student = Student.objects.get(pk=student_id)
        student.is_deleted = True
        student.date_exit = today
        ClassPaymentMaster.objects.filter(student=student,
                                          date_to_pay__gte=now
                                          ).delete()
        attendance_masters = AttendanceMaster.objects.filter(
            class_master=student.class_master,
            date__gte=now
        )
        for attendance_master in attendance_masters:
            attendance_master.attendance_details.filter(student=student).delete()

        student.save()

        return DeleteStudent(success=True)
