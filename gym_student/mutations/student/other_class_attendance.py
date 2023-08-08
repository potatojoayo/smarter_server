import datetime

import graphene

from gym_class.models import AttendanceDetail, ClassDetail, AttendanceMaster
from gym_student.models import Student


class OtherClassAttendance(graphene.Mutation):
    class Arguments:
        student_ids = graphene.List(graphene.Int)
        attendance_master_id = graphene.Int()
    success = graphene.Boolean(default_value=False)
    is_duplicated = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, _, __, student_ids, attendance_master_id):
        now = datetime.datetime.now()
        students = Student.objects.filter(pk__in=student_ids)
        for student in students:
            attendance_master = AttendanceMaster.objects.get(pk=attendance_master_id)
            if AttendanceDetail.objects.filter(attendance_master=attendance_master,
                                                   student=student):
                return OtherClassAttendance(is_duplicated=True)
        for student in students:
            attendance_master = AttendanceMaster.objects.get(pk=attendance_master_id)
            AttendanceDetail.objects.create(attendance_master=attendance_master,
                                                student=student,
                                                type="등원",
                                                date_attended=now)
        return OtherClassAttendance(success=True)
