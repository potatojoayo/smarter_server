import graphene
from graphene import relay

from gym_student.models import AuditionMaster
from gym_student.types.audition_master.audition_master_type import AuditionMasterType
from notification.fields.children_notification_field import ChildrenNotificationField
from notification.fields.gym_notification_field import GymNotificationField
from notification.fields.parent_notification_field import ParentNotificationField
from notification.models.gym_notification_receiver import GymNotificationReceiver
from notification.mutations.create_gym_notification import CreateGymNotification
from notification.mutations.delete_gym_notification import DeleteGymNotification
from notification.mutations.gym_notification_read import GymNotificationRead
from notification.mutations.send_notification_alarm_again import SendNotificationAlarmAgain
from notification.mutations.update_gym_notification import UpdateGymNotification
from notification.types.gym_notification_node import GymNotificationNode
from notification.types.gym_notification_receiver_connection import GymNotificationReceiverConnection
from notification.types.gym_notification_receiver_node import GymNotificationReceiverNode


class Query(graphene.ObjectType):
    audition_schedule = graphene.List(AuditionMasterType, date=graphene.Date())
    my_gym_notifications = GymNotificationField(GymNotificationNode,year=graphene.Int(), month=graphene.Int())
    my_children_notifications = ChildrenNotificationField(GymNotificationNode,year=graphene.Int(), month=graphene.Int())
    notification_by_parent = ParentNotificationField(GymNotificationReceiverNode, year=graphene.Int(), month=graphene.Int())

    @staticmethod
    def resolve_audition_schedule(_, info, date):
        gym = info.context.user.gym
        return AuditionMaster.objects.filter(gym=gym, date_audition=date)


class Mutation(graphene.ObjectType):
    create_gym_notification = CreateGymNotification.Field()
    delete_gym_notification = DeleteGymNotification.Field()
    send_notification_alarm_again = SendNotificationAlarmAgain.Field()
    gym_notification_read = GymNotificationRead.Field()
    update_gym_notification = UpdateGymNotification.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)