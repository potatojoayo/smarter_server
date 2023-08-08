import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

from gym_class.models import ClassDetail, AttendanceDetail, AbsentRequest
from gym_student.methods.gym_send_notification import gym_send_notification


def absent_management():
    now = datetime.datetime.now()
    today = now.today()
    now_date = now.date()
    now_weekday = now.weekday()
    time_start = now + datetime.timedelta(minutes=-30)
    class_details = ClassDetail.objects.filter(day=now_weekday,
                                               hour_start=time_start.hour,
                                               min_start=time_start.minute)
    absent_requests = AbsentRequest.objects.filter(date_created__date=today,
                                                   date_absent=today)
    for class_detail in class_details:
        attendances = AttendanceDetail.objects.filter(attendance_master__class_detail=class_detail,
                                                      type=None, attendance_master__date=now_date)

        for attendance in attendances:
            attendance.type = "결석"
            attendance.absent_reason = "무단결석"
            attendance.save()
            # 알림 메시지 전송 안되도록 수정 ( 주석처리 )
            # gym_send_notification(user=attendance.student, type="결석알림", attendance_hour=now.hour,
            #                       attendance_min=now.minute)

            for absent_request in absent_requests:
                if absent_request.student.id == attendance.student.id:
                    attendance.absent_reason = absent_request.absent_reason
                    attendance.save()

