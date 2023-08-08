from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

from business.models import Subcontractor
from calculate.models.subcontractor_calculate import SubcontractorCalculate
from order.models import OrderDetail
from server.celery import app


@app.task
def calculate_subcontractors():
    subcontractors = Subcontractor.objects.all()
    today = datetime.today()
    if today.day == 16:
        first_day = datetime(today.year, today.month, 1, 0, 0, 0)
        last_day = datetime(today.year, today.month, 16, 0, 0, 0)
    else:
        if today.month - 1 == 0:
            first_day = datetime(today.year - 1, 12, 16, 0, 0, 0)
            last_day = datetime(today.year, 1, 1, 0, 0)
        else:
            first_day = datetime(today.year, today.month - 1, 16, 0, 0, 0)
            last_day = datetime(today.year, today.month, 1, 0, 0, 0)
    for subcontractor in subcontractors:

        works = subcontractor.works.filter(date_created__gte=first_day,
                                           date_created__lt=last_day)
        total_price_work = 0
        total_price_work_labor = 0
        work_amount = works.count()
        order_details = OrderDetail.objects.filter(work__in=works)
        for order_detail in order_details:
            total_price_work += order_detail.price_work
            total_price_work_labor += order_detail.price_work_labor
        SubcontractorCalculate.objects.create(subcontractor=subcontractor,
                                              total_price_work=total_price_work,
                                              total_price_work_labor=total_price_work_labor,
                                              work_amount=work_amount,
                                              date_from=first_day,
                                              date_to=last_day)

    return True

