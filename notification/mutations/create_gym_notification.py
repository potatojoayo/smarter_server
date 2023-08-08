import datetime

import graphene
from dateutil import parser
from graphene_file_upload.scalars import Upload

from gym_class.methods.set_alarm_for_notification import set_alarm_for_notification_main
from gym_class.models import ClassMaster
from gym_student.methods.gym_send_notification import gym_send_notification
from gym_student.models import Student, Parent
from notification.models.gym_notification import GymNotification
from notification.models.gym_notification_images import GymNotificationImages
from notification.models.gym_notification_receiver import GymNotificationReceiver


class CreateGymNotification(graphene.Mutation):
    class Arguments:
        class_master_name = graphene.String()
        title = graphene.String()
        contents = graphene.String()
        images = graphene.List(Upload)
        send_type = graphene.String()
        send_datetime = graphene.String()
        event_date = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, **kwargs):
        class_master_name = kwargs.get('class_master_name')
        title = kwargs.get('title')
        contents = kwargs.get('contents')
        images = kwargs.get('images')
        send_type = kwargs.get('send_type')
        send_datetime = parser.parse(kwargs.get('send_datetime'))
        event_date = parser.parse(kwargs.get('event_date'))
        user = info.context.user
        gym = user.gym
        parent_list = []
        if class_master_name == "전체":
            gym_notification = GymNotification.objects.create(gym=gym,
                                                              title=title,
                                                              contents=contents,
                                                              type="전체",
                                                              send_type=send_type,
                                                              send_datetime=send_datetime,
                                                              event_date=event_date)
            if images:
                for image in images:
                    GymNotificationImages.objects.create(gym_notification=gym_notification,
                                                         image=image)
            class_masters = ClassMaster.objects.filter(gym=gym, is_deleted=False)
            for class_master in class_masters:
                students = Student.objects.filter(class_master=class_master,
                                                  status="수강중")
                for student in students:
                    parent_dic = {'student': student}
                    exist = False
                    for parent in parent_list:
                        if parent['student'].parent == student.parent:
                            exist = True
                    if not exist:
                        parent_list.append(parent_dic)
            if send_type == "즉시":
                now = datetime.datetime.now()
                gym_notification.send_type = "즉시"
                gym_notification.send_datetime = now
            else:
                gym_notification.send_type = "예약"
                gym_notification.send_datetime = send_datetime
            gym_notification.save()

        else:
            class_master = gym.class_masters.get(name=class_master_name)
            gym_notification = GymNotification.objects.create(class_master=class_master,
                                                              gym=gym,
                                                              title=title,
                                                              contents=contents,
                                                              type="클래스",
                                                              send_type=send_type,
                                                              send_datetime=send_datetime
                                                              )
            if images:
                for image in images:
                    GymNotificationImages.objects.create(gym_notification=gym_notification,
                                                         image=image)

            students = Student.objects.filter(class_master=class_master,
                                              status="수강중")
            for student in students:
                parent_dic = {'student': student}
                exist = False
                for parent in parent_list:
                    if parent['student'].parent == student.parent:
                        exist = True
                if not exist:
                    parent_list.append(parent_dic)
            if send_type == "즉시":
                gym_notification.send_type = "즉시"
            else:
                gym_notification.send_type = "예약"
            gym_notification.save()
        if send_type == "즉시":
            for parent in parent_list:
                print(parent)
                GymNotificationReceiver.objects.create(gym_notification=gym_notification,
                                                       parent=parent['student'].parent)
                gym_send_notification(user=parent['student'], type="알림장알림", gym_notification_title=title)
        else:
            gym_id = gym.id
            gym_notification_id = gym_notification.id
            set_alarm_for_notification_main(send_datetime, parent_list, title, gym_id, gym_notification_id)
        return CreateGymNotification(success=True)

