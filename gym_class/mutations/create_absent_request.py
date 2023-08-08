import graphene
from datetime import datetime, timedelta

from authentication.models import User
from gym_class.models import AbsentRequest, AttendanceDetail
from gym_student.methods.gym_send_notification import gym_send_notification
from gym_student.models import Student


class CreateAbsentRequest(graphene.Mutation):
    class Arguments:
        student = graphene.String()
        absent_reason = graphene.String()
        date_absent = graphene.DateTime()
        date_absent_end = graphene.DateTime()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, student, absent_reason, date_absent, date_absent_end):
        """
        now = datetime.now()
        now_time = now.time()
        now_hour = now_time.hour
        now_min = now_time.minute
        today = now.date()
        """
        parent = info.context.user.parent

        student = Student.objects.filter(name=student, parent=parent).first()

        print( type(date_absent), type(date_absent_end) )

        start_date = date_absent
        end_date = date_absent_end + timedelta(days=1)
        print( start_date, end_date )
        gym_send_notification(user=student, type="결석예정 알림", date_absent=date_absent, date_absent_end=date_absent_end)
        while start_date < end_date :
            print( date_absent, start_date, end_date)
            absent_request = AbsentRequest.objects.create(student=student, type="신청", absent_reason=absent_reason,
                                                          date_absent=start_date)
            """
            if today == date_absent:
                attendance_detail = AttendanceDetail.objects.get(student=student,
                                                                 attendance_master__date=date_absent)
                attendance_detail.type = "결석"
                attendance_detail.absent_reason = absent_request.date_absent
                attendance_detail.save()
                gym_send_notification(user=student, type="결석",
                                      attendance_hour=now_hour,
                                      attendance_min=now_min)
            """
            start_date = start_date + timedelta(days=1)


        return CreateAbsentRequest(success=True)
