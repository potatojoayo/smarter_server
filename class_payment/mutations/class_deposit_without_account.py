from datetime import datetime

import graphene
from django.db import transaction

from class_payment.models import ClassPaymentRequest, ClassPaymentMaster
from common.methods.create_notification import create_notification
from common.methods.send_notification import send_notification
from common.methods.get_bank_infos import get_bank_infos
from common.models import BankAccount
from order.models import OrderMaster
from order.models.order_detail import OrderDetail
from order.types.order_master_type import OrderMasterType
from payment.models import PaymentRequest
from smarter_money.models import SmarterMoneyHistory


class ClassDepositWithoutAccount(graphene.Mutation):
    class Arguments:
        class_payment_master_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info,
               class_payment_master_ids,
               ):

        user = info.context.user
        class_payment_masters = ClassPaymentMaster.objects.filter(pk__in=class_payment_master_ids)
        print(class_payment_master_ids)
        for class_payment_master in class_payment_masters:
            class_payment_master.payment_method = '무통장입금'
            class_payment_master.save()
            ClassPaymentRequest.objects.create(method='무통장입금',
                                               amount=class_payment_master.price_to_pay,
                                               orderId=class_payment_master.order_id,
                                               customerName=user.name,
                                               orderName='학원비결제'
                                               )

        return ClassDepositWithoutAccount(success=True)
