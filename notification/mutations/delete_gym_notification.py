import graphene
from datetime import datetime
from notification.models import GymNotification
from scheduler.apps import scheduler
import pytz

class DeleteGymNotification(graphene.Mutation):
    class Arguments:
        gym_notification_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, gym_notification_id):
        timezone_seoul = pytz.timezone('Asia/Seoul')
        now_time = datetime.now()
        now = timezone_seoul.localize(now_time)
        gym = info.context.user.gym
        print(gym_notification_id)
        gym_notification = GymNotification.objects.get(pk=gym_notification_id)
        if gym_notification.send_datetime and gym_notification.send_datetime > now:
            scheduler.remove_job(job_id='set_alarm_for_notification'+str(gym.id)+str(gym_notification_id))
        GymNotification.objects.filter(pk=gym_notification_id).delete()

        return DeleteGymNotification(success=True)
