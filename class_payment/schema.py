from datetime import datetime, date

import graphene
from graphene import relay

from authentication.types import UserType
from class_payment.fields import MyClassPaymentMasterField
from class_payment.fields.is_approved_class_payment_master_field import IsApprovedClassPaymentMasterField
from class_payment.fields.my_gym_class_payment_master_field import MyGymClassPaymentMasterField
from class_payment.models import ClassPaymentMaster
from class_payment.mutations.class_cancel_payment import ClassCancelPayment
from class_payment.mutations.class_deposit_without_account import ClassDepositWithoutAccount
from class_payment.mutations.hello_world import HelloWorld
from class_payment.mutations.is_approved import IsApproved
from class_payment.mutations.paid_check import PaidCheck
from class_payment.mutations.send_class_payment_alarm import SendClassPaymentAlarm
from class_payment.mutations.update_class_payment_master import UpdateClassPaymentMaster
from class_payment.types.class_payment_master.class_payment_master_node import ClassPaymentMasterNode
from class_payment.types.gym_bank_account_type import GymBankAccountType
from class_payment.types.payment_per_month_type import PaymentPerMonthType
from gym_class.models import ClassMaster, AttendanceDetail
from gym_class.types.attendance.attendance_type import AttendanceType


class Query(graphene.ObjectType):
    my_class_payment_masters = MyClassPaymentMasterField(ClassPaymentMasterNode)
    class_payment_master = relay.Node.Field(ClassPaymentMasterNode)
    my_gym_class_payment_masters = MyGymClassPaymentMasterField(ClassPaymentMasterNode, filtering_name=graphene.String(default_value=''), filtering_days=graphene.Int(default_value=3000))
    absent_history = graphene.List(AttendanceType, class_payment_master_id=graphene.Int())
    gym_account_info = graphene.Field(GymBankAccountType)
    payment_per_month = graphene.List(PaymentPerMonthType, year=graphene.Int())
    is_approved_class_payment_masters = IsApprovedClassPaymentMasterField(ClassPaymentMasterNode)
    @staticmethod
    def resolve_payment_per_month(_, info, year):
        gym = info.context.user.gym
        class_masters = gym.class_masters.all()
        gym_created = gym.date_created
        gym_created_year = int(gym_created.strftime('%Y'))
        gym_created_month = int(gym_created.strftime('%m'))
        if year == datetime.today().year:
            month = datetime.today().month
        else:
            month = 12
        payment_list = []
        for i in range(month):
            if date(gym_created_year, gym_created_month, 1) <= date(year, i+1, 1):
                class_payment_masters = ClassPaymentMaster.objects.filter(class_master__in=class_masters,
                                                                          date_paid__year=year,
                                                                          date_paid__month=i+1,
                                                                          payment_status="납부완료")
                amount = 0
                for class_payment_master in class_payment_masters:
                    amount += class_payment_master.price_to_pay
                payment_dic = {
                    'month': i+1,
                    'amount': amount
                }
                payment_list.append(payment_dic)
        return payment_list

    @staticmethod
    def resolve_gym_account_info(_, info):
        parent = info.context.user.parent
        student = parent.students.first()
        gym = student.class_master.gym
        info_dic = {
            'bank_name': gym.refund_bank_name,
            'bank_owner_name': gym.refund_bank_owner_name,
            'bank_account_no': gym.refund_bank_account_no
        }
        return info_dic

    @staticmethod
    def resolve_class_payment_masters(_, info, class_master_id=None, did_paid=None, ):
        gym = info.context.user.gym
        if class_master_id:
            class_masters = ClassMaster.objects.filter(pk=class_master_id, gym=gym)
        else:
            class_masters = gym.class_masters.all()

        if did_paid:
            return ClassPaymentMaster.objects.filter(class_master__in=class_masters,
                                                     did_paid=did_paid)
        else:
            return ClassPaymentMaster.objects.filter(class_master__in=class_masters)

    @staticmethod
    def resolve_class_payment_master(_, __, class_payment_master_id):
        return ClassPaymentMaster.objects.get(pk=class_payment_master_id)

    @staticmethod
    def resolve_absent_history(_, __, class_payment_master_id):
        class_payment_master = ClassPaymentMaster.objects.get(pk=class_payment_master_id)
        student = class_payment_master.student
        return AttendanceDetail.objects.filter(student=student, type='결석',
                                               attendance_master__date__range
                                               =[class_payment_master.date_from, class_payment_master.date_to]
                                               ).exclude(absent_reason='무단결석')

    @staticmethod
    def resolve_payment_by_parent(_, info):
        parent = info.context.user.parent.get()
        return ClassPaymentMaster.objects.filter(student__in=parent.students.all(),
                                                 payment_method="미납")

    @staticmethod
    def resolve_payment_completion_by_parent(_, info, year, month):
        parent = info.context.user.parent.get()
        new_month = 0
        new_year = 0
        if month+1 == 13:
            new_month = 1
            new_year = year+1
        return ClassPaymentMaster.objects.filter(student__in=parent.students.all(),
                                                 payment_status="완납",
                                                 date_paid__lt=datetime(new_year, new_month, 1),
                                                 date_paid__gte=datetime(year, month, 1))
    """
    @staticmethod
    def resolve_class_payment_master_by_parent(_, info):
        parent = info.context.user.parent.get()
        return ClassPaymentMaster.objects.filter(student__parent=parent,
                                                 is_approved=True)
    """

class Mutation(graphene.ObjectType):
    paid_check = PaidCheck.Field()
    class_cancel_payment = ClassCancelPayment.Field()
    class_deposit_without_account = ClassDepositWithoutAccount.Field()
    is_approved = IsApproved.Field()
    update_class_payment_master = UpdateClassPaymentMaster.Field()
    send_class_payment_alarm = SendClassPaymentAlarm.Field()
    hello_world = HelloWorld.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)

