from datetime import datetime
import graphene
from django.db import transaction

from gym_class.models import ClassMaster, ClassDetail, AttendanceMaster
from gym_class.types.classes.class_detail_input_type import ClassDetailInputType
from gym_class.types.classes.class_master_input_type import ClassMasterInputType


class CreateOrUpdateClass(graphene.Mutation):
    class Arguments:
        class_master = ClassMasterInputType()
        weekdays = graphene.List(graphene.Int, required=True)
        class_details = ClassDetailInputType()

    success = graphene.Boolean()
    student_exists = graphene.Boolean(default_value=False)
    is_duplicated = graphene.Boolean(default_value=False)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, **kwargs, ):
        print('버튼클릭됨')
        print(1)
        class_master = kwargs.get('class_master')
        class_details = kwargs.get('class_details')
        weekdays = kwargs.get('weekdays')
        user = info.context.user
        if class_master.id:
            new_class_master = ClassMaster.objects.get(pk=class_master.id)
            if ClassMaster.objects.filter(gym=user.gym, name=class_master.name) and new_class_master.name != class_master.name:
                return CreateOrUpdateClass(success=False, is_duplicated=True)
            if not new_class_master.is_deleted and class_master.is_deleted:
                if new_class_master.students.count() > 0:
                    return CreateOrUpdateClass(success=False, student_exists=True)
            new_class_master.name = class_master.name
            new_class_master.is_deleted = class_master.is_deleted
            new_class_master.save()
            for weekday in weekdays:
                new_class_detail = new_class_master.class_details.filter(day=weekday).first()
                if new_class_detail:
                    new_class_detail.hour_start = class_details.hour_start
                    new_class_detail.min_start = class_details.min_start
                    new_class_detail.hour_end = class_details.hour_end
                    new_class_detail.min_end = class_details.min_end
                    new_class_detail.is_deleted = False
                    new_class_detail.save()
                else:
                    ClassDetail.objects.create(class_master=new_class_master,
                                               day=weekday,
                                               **class_details)
            ## 체크 안된것들은 is_deleted = True
            new_class_master.class_details.exclude(day__in=weekdays).update(is_deleted=True)
        else:
            gym = user.gym
            if ClassMaster.objects.filter(gym=user.gym, name=class_master.name):
                return CreateOrUpdateClass(success=False, is_duplicated=True)
            new_class_master = ClassMaster.objects.create(gym=gym,
                                                          name=class_master.name,
                                                          )
            for weekday in weekdays:
                ClassDetail.objects.create(class_master=new_class_master,
                                           day=weekday,
                                           **class_details
                                           )
        today_date = datetime.today()
        now = datetime.now()
        today = now.weekday()
        today_detail = new_class_master.class_details.filter(day=today)
        if today_detail.exists():
            detail = today_detail.first()
            AttendanceMaster.objects.get_or_create(class_master=new_class_master,
                                                   class_detail=detail,
                                                   gym=user.gym,
                                                   date=today_date)
        return CreateOrUpdateClass(success=True)
