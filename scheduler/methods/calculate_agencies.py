from django.utils import timezone

from django.conf import settings
from django.utils.datetime_safe import datetime
from django_apscheduler.jobstores import DjangoJobStore

from business.models import Agency
from calculate.models.agency_calculate import AgencyCalculate
from apscheduler.schedulers.background import BackgroundScheduler

from server.celery import app


@app.task
def calculate_agencies():
    today = timezone.localtime()
    agencies = Agency.objects.all()
    for agency in agencies:
        # 총 매출 금액
        price_total_sell = 0
        profit_total = 0
        # 총 환불 금액
        price_refund_total_sell = 0
        profit_refund_total = 0

        if today.day == 16:
            first_day = datetime(today.year, today.month, 1, 0, 0, 0)
            last_day = datetime(today.year, today.month, 16, 0, 0, 0)
        else:
            if today.month - 1 == 0:
                first_day = datetime(today.year-1, 12, 16, 0, 0, 0)
                last_day = datetime(today.year, 1, 1, 0, 0)
            else:
                first_day = datetime(today.year,  today.month-1, 16, 0, 0, 0)
                last_day = datetime(today.year, today.month, 1, 0, 0, 0)

        for gym in agency.gyms.all():
            user = gym.user

            order_masters = user.orders.filter(date_created__gte=first_day,
                                               date_created__lt=last_day)
            for order_master in order_masters:
                for order_detail in order_master.details.all():
                    if order_detail.state not in ["신규주문", "무통장입금","결제완료"]:
                        price_total_sell += order_detail.price_products
                        profit_total += order_detail.price_products - order_detail.price_total_vendor

            claims = user.claims.filter(date_created__gte=first_day,
                                        date_created__lt=last_day)
            for claim in claims:
                if claim.state == "환불완료":
                    order_detail = claim.order_detail
                    price_refund_total_sell += order_detail.price_products
                    profit_refund_total += order_detail.price_products - order_detail.price_total_vendor

        agency_total_sell = price_total_sell-price_refund_total_sell
        price_profit = profit_total-profit_refund_total
        price_platform = price_profit * 0.3
        AgencyCalculate.objects.create(agency=agency, agency_total_sell=agency_total_sell,
                                       price_profit=price_profit,
                                       price_platform=price_platform, date_from=first_day, date_to=last_day,
                                       )












