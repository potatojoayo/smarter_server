import datetime

import graphene

from business.models import Agency
from business.types import SubcontractorType
from order.models import Work, OrderDetail, OrderMaster, Claim
from payment.models import PaymentSuccess, CancelSuccess
from smarter_money.models import SmarterMoneyHistory

from statistic.types.agencies_statistics_connection import AgenciesStatisticsConnection
from statistic.types.agencies_statistics_type import FirstInnerItem
from statistic.types.gyms_statistics_connection import GymsStatisticsConnection

from statistic.types.iris_statistics_type import IrisStatisticsType
from statistic.types.product_statistics_connection import ProductStatisticsConnection
from statistic.types.agencies_statistics_type import AgenciesStatisticsType
from graphene import relay
from pprint import pprint

from statistic.types.subcontractor_statistics_connection import SubcontractorStatisticsConnection


class Query(graphene.ObjectType):
    product_statistics = relay.ConnectionField(ProductStatisticsConnection,
                                                brand_name=graphene.List(graphene.String),
                                                category_name=graphene.List(graphene.String),
                                                sub_category_name=graphene.List(graphene.String),
                                                date_from=graphene.Date(),
                                                date_to=graphene.Date())
    subcontractor_statistics = relay.ConnectionField(SubcontractorStatisticsConnection,
                                                     subcontractors_name=graphene.List(graphene.String),
                                                     date_from=graphene.Date(),
                                                     date_to=graphene.Date())

    iris_sales_statistics = graphene.Field(IrisStatisticsType,
                                           date_from=graphene.Date(),
                                           date_to=graphene.Date())
    agencies_statistics = relay.ConnectionField(AgenciesStatisticsConnection,
                                                date_from=graphene.Date(),
                                                date_to=graphene.Date())
    """agencies_statistics = graphene.List(AgenciesStatisticsConnection,
                                         date_from=graphene.Date(),
                                         date_to=graphene.Date()
                                         )"""
    """agencies_statistics = graphene.List(AgenciesStatisticsType,
                                        date_from=graphene.Date(),
                                        date_to=graphene.Date()
                                        )
    """
    """gyms_statistics = graphene.List(GymsStatisticsType,
                                    date_from=graphene.Date(),
                                    date_to=graphene.Date()
                                    )"""
    gyms_statistics = relay.ConnectionField(GymsStatisticsConnection,
                                                date_from=graphene.Date(),
                                                date_to=graphene.Date())

    def resolve_product_statistics(_, __, brand_name=None,
                                   category_name=None,
                                   sub_category_name=None,
                                   date_from=None,
                                   date_to=None):
        # 상품별 누적 판매금액 설정
        product_list = []
        date_from = date_from + datetime.timedelta(days=-1)
        date_to = date_to + datetime.timedelta(days=1)
        try:
            order_masters = OrderMaster.objects.filter(date_created__range=[date_from, date_to])
            # 조건에 때른 해당 order_detail 가져오기
            order_details = OrderDetail.objects.filter(product_master__brand__name__in=brand_name
                                                       ,product_master__category__name__in=category_name
                                                       ,product_master__sub_category__name__in=sub_category_name
                                                       ,order_master__in=order_masters).exclude(state__in=["반품완료","무통장입금","결제완료"])

            for order_detail in order_details:
                product_dic = {'product':order_detail.product,
                               'product_name': order_detail.product.name,
                               'brand_name': order_detail.product.product_master.brand.name,
                               'category_name': order_detail.product.product_master.category.name,
                               'sub_category_name': order_detail.product.product_master.sub_category.name,
                               'amount': order_detail.price_products,
                               'date_from': str(date_from + datetime.timedelta(days=1)),
                               'date_to': str(date_to + datetime.timedelta(days=-1))
                               }
                exist = False
                for p in product_list:
                    if p['product'].id == product_dic['product'].id:
                        p['amount'] += order_detail.price_products
                        exist = True
                if not exist:
                    product_list.append(product_dic)
        except:
            pass
        #환불한 금액에서 뺴기
        try:
            claims = Claim.objects.filter(date_created__range=[date_from, date_to], state="환불완료")
            for claim in claims:
                product = claim.order_detail.product
                for p in product_list:
                    if p['product'] == product:
                        p['amount'] -= claim.return_price
        except:
            pass
        print(product_list)
        return product_list

    @staticmethod
    def resolve_subcontractor_statistics(_, __, subcontractors_name=None, date_from=None, date_to=None):
        # 해당 기간 작업들 다 가져오기
        date_from = date_from + datetime.timedelta(days=-1)
        date_to = date_to + datetime.timedelta(days=1)
        works = Work.objects.filter(subcontractor__name__in=subcontractors_name,
                                    date_created__range=[date_from, date_to])
        subcontractor_list = []
        for work in works:
            for order_detail in work.details.all():
                subcontractor_dic = {'subcontractor_name': order_detail.work.subcontractor.name,
                                     'total_price_work': order_detail.price_work,
                                     'total_price_work_labor': order_detail.price_work_labor,
                                     'date_from': str(date_from + datetime.timedelta(days=1)),
                                     'date_to': str(date_to + datetime.timedelta(days=-1)),
                                     'work_amount': 1}
                exist = False
                for sub in subcontractor_list:
                    if sub['subcontractor_name'] == subcontractor_dic['subcontractor_name']:
                        sub['total_price_work'] += subcontractor_dic['total_price_work']
                        sub['total_price_work_labor'] += subcontractor_dic['total_price_work_labor']
                        sub['work_amount'] += 1
                        exist = True
                if not exist:
                    subcontractor_list.append(subcontractor_dic)

        return subcontractor_list


    @staticmethod
    def resolve_iris_sales_statistics(_, __, date_from=None, date_to=None,):
        date_from = date_from + datetime.timedelta(days=-1)
        date_to = date_to + datetime.timedelta(days=1)
        order_masters = OrderMaster.objects.filter(date_created__range=[date_from, date_to])
        total_cash_payment = 0 # 무통장총액
        total_card_payment = 0 # 카드총액
        total_bank_account_payment = 0 # 계좌이체 총액
        total_smarter_money_payment = 0 # 스마터머니 총액
        total_payment = 0 # 결제총액
        refund_amount = 0  # 취소/반품 금액
        total_sales_payment = 0  # 총 결제금액
        total_profit_amount = 0  # 이리스 매출이익 (체육관 공급가 - 이리스 공급가)
        total_product_price = 0  # 상품금액
        total_work_price = 0  # 작업비
        total_work_labor_price = 0  # 작업용역비
        total_order_price = 0  # 상품주문금액
        total_delivery_price = 0  # 배송비
        total_price = 0 # 총 매출액
        for order_master in order_masters:
            # <<----------->> : 결제수단별 내역
            payment_success = PaymentSuccess.objects.get(orderId=order_master.order_number)
            smarter_money = SmarterMoneyHistory.objects.get(order_master=order_master,
                                                            transaction_type="사용")
            if payment_success.method == "카드":
                total_card_payment += payment_success.totalAmount
            elif payment_success.method == "계좌이체":
                total_bank_account_payment += payment_success.totalAmount
            elif payment_success.method == "무통장입금":
                total_cash_payment += payment_success.totalAmount
            total_smarter_money_payment += smarter_money.amount
            total_payment += total_card_payment + total_bank_account_payment + total_cash_payment
            total_delivery_price += order_master.price_delivery

            # <<----------->> : 취소/반품 내역
            # << 취소 >>
            try:
                cancels = CancelSuccess.objects.filter(paymentSuccess=payment_success)
                for cancel in cancels:
                    refund_amount += cancel.cancelAmount
            except:
                pass
            order_details = OrderDetail.objects.filter(order_master=order_master).exclude(
                state__in=["반품완료", "무통장입금", "결제완료"])
            # << 환불 >>
            try:
                claims = Claim.objects.filter(order_detail__in=order_details)
                for claim in claims:
                    refund_amount += claim.return_price
            except:
                pass

            for order_detail in order_details:
                total_profit_amount += (order_detail.price_gym - order_detail.price_vendor)*order_detail.quantity
                # 총 매출이익에서 환불한거 빼주기
                try:
                    claims = Claim.objects.filter(order_detail=order_detail)
                    for claim in claims :
                        total_profit_amount -= (claim.order_detail.price_gym-claim.order_detail.price_vendor)*claim.quantity
                except:
                    pass
                total_product_price += order_detail.price_products
                total_work_price += order_detail.price_work
                total_work_labor_price += order_detail.price_work_labor
                total_order_price += total_product_price + total_work_price
            total_price = total_order_price + total_delivery_price
        # 총 결제금액
        total_payment = total_sales_payment - refund_amount
        iris_sales_dic = {
            'total_cash_payment': total_cash_payment,
            'total_card_payment': total_card_payment,
            'total_bank_account_payment': total_bank_account_payment,
            'total_smarter_money_payment': total_smarter_money_payment,
            'total_payment': total_payment,
            'refund_amount': refund_amount,
            'total_sales_payment': total_sales_payment,
            'total_profit_amount': total_profit_amount,
            'total_product_price': total_product_price,
            'total_work_price': total_work_price,
            'total_work_labor_price': total_work_labor_price,
            'total_order_price': total_order_price,
            'total_delivery_price': total_delivery_price,
            'total_price': total_price,
            'date_from': str(date_from + datetime.timedelta(days=1)),
            'date_to': str(date_to + datetime.timedelta(days=-1))
        }
        return iris_sales_dic

    @staticmethod
    def resolve_agencies_statistics(_, __, date_from=None, date_to=None, ):
        agency_statistics = []
        agency_dic = {}
        agencies = Agency.objects.all()
        for agency in agencies:
            without_account_payment = 0 #무통장
            card_payment = 0 #카드
            bank_payment = 0 #계좌이체
            smarter_money_amount = 0 #스마터머니
            refund_amount = 0 #취소/반품 금액
            gyms = agency.gyms.all()
            for gym in gyms:
                order_masters = gym.user.orders.filter(date_created__range=[date_from, date_to])
                for order_master in order_masters:
                    payment_success = PaymentSuccess.objects.get(orderId=order_master.order_number)
                    method = payment_success.method
                    amount = payment_success.totalAmount
                    try:
                        smarter_money = SmarterMoneyHistory.objects.get(order_master=order_master,
                                                                        transaction_type="사용")
                        smarter_money_amount += smarter_money.amount
                    except:
                        pass
                    if method == "카드" :
                        card_payment += amount
                    elif method == "계좌이체":
                        bank_payment += amount
                    elif method == "무통장":
                        without_account_payment += amount
                    # <<----------->> : 취소/반품 내역
                    # << 취소 >>
                    try:
                        cancels = CancelSuccess.objects.filter(paymentSuccess=payment_success)
                        for cancel in cancels:
                            refund_amount += cancel.cancelAmount
                    except:
                        pass
                    order_details = OrderDetail.objects.filter(order_master=order_master).exclude(
                        state__in=["반품완료", "무통장입금", "결제완료"])
                    # << 환불 >>
                    try:
                        claims = Claim.objects.filter(order_detail__in=order_details)
                        for claim in claims:
                            refund_amount += claim.return_price
                    except:
                        pass
            # 결제 총액
            total_payment = smarter_money_amount + card_payment + bank_payment + without_account_payment
            # 총 매출액 ( 결제총액 - 취소/반품 금액 )
            total_amount = total_payment - refund_amount
            agency_name = str(agency.name)
            """agency_dic[agency_name] = {
                'without_bank_payment': without_account_payment,
                'card_payment': card_payment,
                'bank_payment': bank_payment,
                'smarter_money_amount': smarter_money_amount,
                'total_payment': total_payment,
                'refund_amount': refund_amount,
                'total_amount': total_amount
            }"""
            agency_dic = {
                agency_name: {
                    'without_bank_payment': without_account_payment,
                    'card_payment': card_payment,
                    'bank_payment': bank_payment,
                    'smarter_money_amount': smarter_money_amount,
                    'total_payment': total_payment,
                    'refund_amount': refund_amount,
                    'total_amount': total_amount
                },
                '123': {
                    'without_bank_payment': without_account_payment,
                    'card_payment': card_payment,
                    'bank_payment': bank_payment,
                    'smarter_money_amount': smarter_money_amount,
                    'total_payment': total_payment,
                    'refund_amount': refund_amount,
                    'total_amount': total_amount
                }
            }
            agency_statistics = []
            for agency_name, value in agency_dic.items():
                first_inner_item = FirstInnerItem(value['without_bank_payment'],
                                                  value['card_payment'],
                                                  value['bank_payment'],
                                                  value['smarter_money_amount'],
                                                  value['total_payment'],
                                                  value['refund_amount'],
                                                  value['total_amount']
                                                  )
                dictionary = AgenciesStatisticsType(agency_name, first_inner_item)
                #dictionary = AgenciesStatisticsConnection(agency_type)
                agency_statistics.append(dictionary)
            print(agency_statistics)
        return agency_statistics

    @staticmethod
    def resolve_gyms_statistics(_, __, date_from=None, date_to=None, ):
        agencies = Agency.objects.all()
        gym_list = []
        for agency in agencies:
            gyms = agency.gyms.all()

            for gym in gyms:
                without_account_payment = 0  # 무통장
                card_payment = 0  # 카드
                bank_payment = 0  # 계좌이체
                smarter_money_amount = 0  # 스마터머니
                refund_amount = 0  # 취소/반품 금액

                order_masters = gym.user.orders.filter(date_created__range=[date_from, date_to])
                for order_master in order_masters:
                    payment_success = PaymentSuccess.objects.get(orderId=order_master.order_number)
                    method = payment_success.method
                    amount = payment_success.totalAmount
                    try:
                        smarter_money = SmarterMoneyHistory.objects.get(order_master=order_master,
                                                                        transaction_type="사용")
                        smarter_money_amount += smarter_money.amount
                    except:
                        pass
                    if method == "카드":
                        card_payment += amount
                    elif method == "계좌이체":
                        bank_payment += amount
                    elif method == "무통장":
                        without_account_payment += amount
                    # <<----------->> : 취소/반품 내역
                    # << 취소 >>
                    try:
                        cancels = CancelSuccess.objects.filter(paymentSuccess=payment_success)
                        for cancel in cancels:
                            refund_amount += cancel.cancelAmount
                    except:
                        pass
                    order_details = OrderDetail.objects.filter(order_master=order_master).exclude(
                        state__in=["반품완료", "무통장입금", "결제완료"])
                    # << 환불 >>
                    try:
                        claims = Claim.objects.filter(order_detail__in=order_details)
                        for claim in claims:
                            refund_amount += claim.return_price
                    except:
                        pass
            # 결제 총액
                total_payment = smarter_money_amount + card_payment + bank_payment + without_account_payment
            # 총 매출액 ( 결제총액 - 취소/반품 금액 )
                total_amount = total_payment - refund_amount
                gym_dic = {
                    'agency_name': agency.name,
                    'gym_name': gym.name,
                    'without_bank_payment': without_account_payment,
                    'card_payment': card_payment,
                    'bank_payment': bank_payment,
                    'smarter_money_amount': smarter_money_amount,
                    'total_payment': total_payment,
                    'refund_amount': refund_amount,
                    'total_amount': total_amount
                }
                gym_list.append(gym_dic)
        print(gym_list)
        return gym_list


schema = graphene.Schema(query=Query)
