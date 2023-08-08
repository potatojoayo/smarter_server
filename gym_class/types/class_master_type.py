from datetime import datetime

import graphene
from graphene_django import DjangoObjectType

from gym_class.models.class_master import ClassMaster
from gym_class.types.class_detail_type import ClassDetailType


class ClassMasterType(DjangoObjectType):

    class Meta:
        model = ClassMaster

    class_details = graphene.List(ClassDetailType)
    current_class_detail = graphene.Field(ClassDetailType)
    week_days = graphene.List(graphene.Int)

    @staticmethod
    def resolve_week_days(root, _):
        class_details = root.class_details.filter(is_deleted=False)
        week_days = []
        for class_detail in class_details:
            week_days.append(class_detail.day)
        return week_days

    @staticmethod
    def resolve_class_details(root, _):
        return root.class_details.filter(is_deleted=False).order_by('day')

    @staticmethod
    def resolve_current_class_detail(root, _):
        now = datetime.now()
        today = datetime.today().weekday()
        details = root.class_details.filter(day=today)
        for detail in details:
            start_time = now.replace(hour=detail.hour_start, minute=detail.min_start)
            end_time = now.replace(hour=detail.hour_end, minute=detail.min_end)
            if now <= end_time:
                print(detail)
                print('0000')
                return detail
        return None





