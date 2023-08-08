from datetime import datetime

import graphene
from django.db import transaction

from gym_class.models import ClassMaster, ClassDetail, AttendanceMaster


class NewCreateClass(graphene.Mutation):
    class Arguments:
        class_master_name = graphene.String()
        weekdays = graphene.List(graphene.Int,required=True)
        hour_start = graphene.Int(required=True)
        min_start = graphene.Int(required=True)
        hour_end = graphene.Int(required=True)
        min_end = graphene.Int(required=True)
        class_master_is_deleted = graphene.Boolean(default_value=False)
        class_detail_is_deleted = graphene.Boolean(default_value=False)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, class_master_name, weekdays,
               hour_start, min_start, hour_end, min_end,
               class_master_is_deleted, class_detail_is_deleted):

        user = info.context.user
        gym = user.gym

        class_master = ClassMaster.objects.create(gym=gym,
                                                  name=class_master_name,
                                                  is_deleted=class_master_is_deleted)
        for weekday in weekdays:
            ClassDetail.objects.create(class_master=class_master,
                                       day=weekday,
                                       hour_start=hour_start,
                                       min_start=min_start,
                                       hour_end=hour_end,
                                       min_end=min_end,
                                       is_deleted=class_detail_is_deleted)
        today_date = datetime.today()
        now = datetime.now()
        today = now.weekday()
        today_detail = class_master.class_details.filter(day=today)
        if today_detail.exists():
            detail = today_detail.first()
            AttendanceMaster.objects.get_or_create(class_master=class_master,
                                                   class_detail=detail,
                                                   gym=user.gym,
                                                   date=today_date)
        return NewCreateClass(success=True)

