from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore

from authentication.models import User
from common.models import Membership
from server.celery import logger


def update_membership():
    logger.info("Starting update_membership")
    normal_member = Membership.objects.get(name="일반회원")
    good_member = Membership.objects.get(name="우수회원")
    best_member = Membership.objects.get(name="최우수회원")
    good_member_condition = good_member.condition
    best_member_condition = best_member.condition
    for user in User.objects.filter(groups__name__contains='체육관'):
        try:
            gym = user.gym
            logger.info(gym)
            if best_member_condition <= gym.total_purchased_amount:
                logger.info('best_member_condition <= gym.total_purchased_amount')
                gym.membership = best_member
                gym.save()
            elif good_member_condition <= gym.total_purchased_amount < best_member_condition:
                logger.info('good_member_condition <= gym.total_purchased_amount < best_member_condition')
                gym.membership = good_member
                gym.save()
            else:
                logger.info('else')
                gym.membership = normal_member
                gym.save()
        except:
            continue
