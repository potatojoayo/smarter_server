from datetime import datetime

import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from gym_class.models import ClassMaster, AttendanceDetail, AttendanceMaster
from gym_student.methods.gym_send_notification import gym_send_notification
from gym_student.models import Student


class AttendanceForStudent(graphene.Mutation):
    class Arguments:
        class_master_id = graphene.Int()
        student_id = graphene.Int()

    success = graphene.Boolean()
    already_attended = graphene.Boolean(default_value=False)
    type = graphene.String()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, **kwargs):
        now = datetime.now()
        now_time = now.time()
        now_time_hour = now_time.hour
        now_time_min = now_time.minute
        class_master_id = kwargs.get('class_master_id')
        student_id = kwargs.get('student_id')
        print(kwargs)
        print(class_master_id)
        print(student_id)

        student = Student.objects.get(pk=student_id)

        class_master = ClassMaster.objects.get(pk=class_master_id)

        attendance_master = AttendanceMaster.objects.get(date=now, class_master=class_master)
        attendance_details = attendance_master.attendance_details.filter(
            attendance_master__class_master=class_master,
            student=student)
        if attendance_details.exists():
            attendance_detail = attendance_details.first()
            # if class_master_id == student.class_master_id:

            if attendance_detail.type == '등원':
                already_attended = True
            elif attendance_detail.type == '타수업등원':
                already_attended = True
            else:
                attendance_detail.type = '등원'
                attendance_detail.date_attended = now
                attendance_detail.save()
                already_attended = False

                gym_send_notification(user=student, type="등원알림", attendance_hour=now_time_hour,
                                      attendance_min=now_time_min)
            return AttendanceForStudent(success=True, type="등원", already_attended=already_attended)


        else:
            _, created = AttendanceDetail.objects.get_or_create(attendance_master=attendance_master,
                                                                student=student,
                                                                # type="타수업등원",
                                                                type="등원",
                                                                date_attended=now
                                                                )
            gym_send_notification(user=student, type="등원알림", attendance_hour=now_time_hour,
                                  attendance_min=now_time_min)
            return AttendanceForStudent(success=True, type="타수업등원", already_attended=not created)
    # try:
    #     attendance_master = AttendanceMaster.objects.get(date=now, class_master=class_master)
    #     attendance_detail = attendance_master.attendance_details.get(attendance_master__class_master=class_master,
    #                                                                  student=student)
    # except ObjectDoesNotExist:
    #     return AttendanceForStudent(success=False)
    # attendance_detail.date_attended = now
    # attendance_detail.type = '등원'
    # attendance_detail.save()
    # gym_send_notification(user=student, type="등원알림", attendance_hour=now_time_hour, attendance_min=now_time_min)
    # return AttendanceForStudent(success=True)
