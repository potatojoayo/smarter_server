import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

from gym_class.models import ClassDetail, AttendanceDetail, AbsentRequest, AttendanceMaster
from server.celery import logger


def attendance_management():
    logger.info('starting attendance_management')
    today = datetime.date.today()
    today_day = datetime.datetime.today().weekday()
    class_details = ClassDetail.objects.filter(day=today_day, is_deleted=False)
    logger.info('class_details')
    logger.info(class_details)
    for class_detail in class_details:
        attendance_master, created = AttendanceMaster.objects.get_or_create(class_master=class_detail.class_master,
                                        class_detail=class_detail,
                                        gym=class_detail.class_master.gym,
                                        date=today)
    class_master_student_list = []
    absent_request_student_ids = []
    absent_requests = AbsentRequest.objects.filter(date_absent=today)
    for absent_request in absent_requests:
        absent_request_student_ids.append(absent_request.student.id)
    logger.info('absent_request_student_ids')
    logger.info(absent_request_student_ids)
    for class_detail in class_details:
        students = class_detail.class_master.students.filter(status="수강중")
        for student in students:
            if student.date_entered <= today:
                class_master_student_dic = {
                    'student': student,
                    'class_master': student.class_master,
                    'class_detail': class_detail
                }
                exist = False
                for class_master_student in class_master_student_list:
                    if class_master_student['student'].id == class_master_student_dic['student'].id:
                        exist = True
                if not exist:
                    class_master_student_list.append(class_master_student_dic)
    logger.info('class_master_student_list')
    logger.info(class_master_student_list)
    for class_master_student in class_master_student_list:
        attendance_master = AttendanceMaster.objects.get(
            class_master=class_master_student['class_master'],
            class_detail=class_master_student['class_detail'],
            gym=class_master_student['class_master'].gym,
            date=today)
        logger.info('attendance_master')
        logger.info(attendance_master)
        logger.info('class_master_student')
        logger.info(class_master_student)
        attendance_detail = AttendanceDetail.objects.create(student=class_master_student['student'],
                                                            attendance_master=attendance_master)
        for absent_request in absent_requests:
            if absent_request.student == attendance_detail.student:
                logger.info('absent_request.student')
                logger.info(absent_request.student)
                logger.info('attendance_detail.student')
                logger.info(attendance_detail.student)
                attendance_detail.type = absent_request.type
                attendance_detail.absent_reason = absent_request.absent_reason
                attendance_detail.save()

    logger.info('finishing attendance_management')