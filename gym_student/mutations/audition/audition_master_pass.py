from datetime import datetime

import graphene

from dateutil import parser

from gym_student.methods.audition_result_alarm import audition_result_alarm_main
from gym_student.methods.gym_send_notification import gym_send_notification
from gym_student.models import AuditionMaster, AuditionDetail

class AuditionMasterPass(graphene.Mutation):
    class Arguments:
        audition_master_id = graphene.Int()
        estimated_alarm_date = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info,audition_master_id, estimated_alarm_date):
        gym = info.context.user.gym
        now = datetime.now()
        audition_master = AuditionMaster.objects.get(pk=audition_master_id)
        audition_master.estimated_alarm_date = parser.parse(estimated_alarm_date)
        audition_master.state = "완료"
        audition_master.save()
        ###### 지금 보내는 로직 ######
        get_date = parser.parse(estimated_alarm_date)
        audition_master = AuditionMaster.objects.get(pk=audition_master_id)
        audition_details = AuditionDetail.objects.filter(audition_master=audition_master)
        if (datetime(get_date.year, get_date.month, get_date.day, get_date.hour, get_date.minute)
            == datetime(now.year, now.month, now.day, now.hour, now.minute)):
            for audition_detail in audition_details:
                did_pass = audition_detail.did_pass
                if did_pass:
                    gym_send_notification(user=audition_detail.student.parent.user, type="승급 완료 알림",
                                          audition_detail=audition_detail)
                else:
                    gym_send_notification(user=audition_detail.student.parent.user, type="승급 실패 알림",
                                          audition_detail=audition_detail)
        else:
            gym_id = gym.id
            audition_result_alarm_main(estimated_alarm_date, audition_master_id, gym_id)
        return AuditionMasterPass(success=True)