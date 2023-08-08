from datetime import datetime

import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from gym_class.models import ClassMaster, AttendanceDetail, AttendanceMaster
from gym_student.methods.gym_send_notification import gym_send_notification
from gym_student.models import Student


class AttendanceForAllClasses(graphene.Mutation):
    class Arguments:
        class_master_id = graphene.Int()
        student_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, **kwargs):
        now = datetime.now()
        now_time = now.time()
        now_time_hour = now_time.hour
        now_time_min = now_time.minute
        class_master_id = kwargs.get('class_master_id')
        print(class_master_id)
        student_id = kwargs.get('student_ids')
        print(student_id)
        student = Student.objects.get(pk=student_id)

        class_master = ClassMaster.objects.get(pk=class_master_id)

        try:
            attendance_master = AttendanceMaster.objects.get(date=now, class_master=class_master)
            attendance_detail = attendance_master.attendance_details.get(
                attendance_master__class_master=class_master,
                student=student)
        except ObjectDoesNotExist:
            return AttendanceForAllClasses(success=False)

        if class_master_id == student.class_master_id:

            attendance_detail.type = '등원'
            attendance_detail.save()
            gym_send_notification(user=student, type="등원알림", attendance_hour=now_time_hour, attendance_min=now_time_min)
            return AttendanceForAllClasses(success=True, type="등원")

        else:
            AttendanceDetail.objects.create(attendance_master=attendance_master,
                                            student=student,
                                            # type="타수업등원",
                                            type="등원",
                                            date_attended=now)
            return AttendanceForAllClasses(success=True, type="타수업등원")




        # try:
        #     attendance_master = AttendanceMaster.objects.get(date=now, class_master=class_master)
        #     attendance_detail = attendance_master.attendance_details.get(attendance_master__class_master=class_master,
        #                                                                  student=student)
        # except ObjectDoesNotExist:
        #     return AttendanceForAllClasses(success=False)
        # attendance_detail.date_attended = now
        # attendance_detail.type = '등원'
        # attendance_detail.save()
        # gym_send_notification(user=student, type="등원알림", attendance_hour=now_time_hour, attendance_min=now_time_min)
        # return AttendanceForAllClasses(success=True)
