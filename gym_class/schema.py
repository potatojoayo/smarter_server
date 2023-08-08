from datetime import datetime, timedelta

import graphene
from graphene import relay

from gym_class.fields.attendance_field import AttendanceField
from gym_class.fields.my_children_attendance_field import MyChildrenAttendanceField
from gym_class.models import AttendanceDetail, AttendanceMaster, ClassDetail, AbsentRequest
from gym_class.mutations.classes.new_create_class import NewCreateClass
from gym_class.mutations.level.change_level_order import ChangeLevelOrder
from gym_class.mutations.create_absent_request import CreateAbsentRequest
from gym_class.models import Level, ClassMaster
from gym_class.mutations.classes.create_or_update_class import CreateOrUpdateClass
from gym_class.mutations.classes.delete_class_detail import DeleteClassDetail
from gym_class.mutations.classes.delete_class_master import DeleteClassMaster
from gym_class.mutations.delete_absent_request import DeleteAbsentRequest
from gym_class.mutations.level.create_or_update_level import CreateOrUpdateLevel
from gym_class.mutations.level.delete_level import DeleteLevel
from gym_class.mutations.test import Test
from gym_class.types import ClassMasterType, LevelType, ClassDetailType
from gym_class.types.absent_request_type import AbsentRequestType
from gym_class.types.attendance.attendance_master_node import AttendanceMasterNode
from gym_student.models import Student


class Query(graphene.ObjectType):
    my_classes = graphene.List(ClassMasterType)
    class_master = graphene.Field(ClassMasterType, id=graphene.Int())
    my_levels = graphene.List(LevelType)
    level = graphene.Field(LevelType, id=graphene.Int())
    attendance_masters = AttendanceField(AttendanceMasterNode)
    attendance_master = relay.Node.Field(AttendanceMasterNode)
    my_children_attendances = MyChildrenAttendanceField(AttendanceMasterNode, year=graphene.Int(), month=graphene.Int())
    my_absent_requests = graphene.List(AbsentRequestType, year=graphene.Int(), month=graphene.Int())
    class_details = graphene.List(ClassDetailType, class_master_id=graphene.Int())
    current_classes = graphene.List(ClassMasterType)
    student_today_classes = graphene.List(ClassDetailType, student_id=graphene.Int())

    @staticmethod
    def resolve_student_today_classes(_, __, student_id):
        now = datetime.now()
        student = Student.objects.get(pk=student_id)
        class_details = student.class_master.class_details.filter(day=now.weekday(), is_deleted=False)
        result = []
        for class_detail in class_details:
            end_time = now.replace(hour=class_detail.hour_end, minute=class_detail.min_end)
            if now <= end_time:
                print(class_detail.class_master.id)
                result.append(class_detail)
        print(result)
        return result

    @staticmethod
    def resolve_current_classes(_, info):
        gym = info.context.user.gym
        print(gym)
        now = datetime.now()
        class_masters = ClassMaster.objects.filter(
            gym=gym,
            is_deleted=False
        )
        results = []
        for class_master in class_masters:
            class_details = class_master.class_details.filter(day=now.weekday(), is_deleted=False)
            for detail in class_details:
                start_time = now.replace(hour=detail.hour_start, minute=detail.min_start)
                end_time = now.replace(hour=detail.hour_end, minute=detail.min_end)
                if start_time - timedelta(hours=4) <= now <= start_time + timedelta(minutes=30):
                    results.append(class_master)
        return results

    @staticmethod
    def resolve_my_absent_requests(_, info, year, month):
        parent = info.context.user.parent
        students = parent.students.all()
        return AbsentRequest.objects.filter(student__in=students, date_absent__year=year, date_absent__month=month) \
            .distinct()

    @staticmethod
    def resolve_class_master(_, __, id):
        return ClassMaster.objects.get(pk=id)

    @staticmethod
    def resolve_my_classes(_, info):
        gym = info.context.user.gym
        return gym.class_masters.filter(is_deleted=False).order_by('-date_created')

    @staticmethod
    def resolve_class_details(_, __, class_master_id):
        class_master = ClassMaster.objects.get(pk=class_master_id)
        return ClassDetail.objects.filter(class_master=class_master)

    @staticmethod
    def resolve_my_levels(_, info):
        gym = info.context.user.gym
        return Level.objects.filter(gym=gym).order_by('order')

    @staticmethod
    def resolve_level(_, __, id):
        return Level.objects.get(pk=id)

    @staticmethod
    def resolve_attendance(_, __, attendance_master_id):
        attendance_master = AttendanceMaster.objects.get(pk=attendance_master_id)
        return AttendanceDetail.objects.filter(attendance_master=attendance_master)

    @staticmethod
    def resolve_attendance_master(_, __, class_master_id):
        class_master = ClassMaster.objects.get(pk=class_master_id)
        return AttendanceMaster.objects.filter(class_master=class_master)


class Mutation(graphene.ObjectType):
    create_or_update_class = CreateOrUpdateClass.Field()
    delete_class_detail = DeleteClassDetail.Field()
    delete_class_master = DeleteClassMaster.Field()
    create_or_update_level = CreateOrUpdateLevel.Field()
    delete_level = DeleteLevel.Field()
    change_level_order = ChangeLevelOrder.Field()
    create_absent_request = CreateAbsentRequest.Field()
    delete_absent_request = DeleteAbsentRequest.Field()
    # new_create_class = NewCreateClass.Field()
    test = Test.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
