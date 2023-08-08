from django.contrib.auth.models import Group
from django.db import transaction

from authentication.models import User
from business.models import Gym, TaFirm


@transaction.atomic()
def run():
    group_ta = Group.objects.create(name="TA상사")
    group_gym = Group.objects.get(name="체육관")

    user_ta = User.objects.create_user(identification="ta1", name="ta1", phone="01000000000",
                                       password="ta1")
    gym = Gym.objects.create(user=user_ta, name="gym_ta1", address="address", detail_address="detail_address",
                             zip_code="zip_code", email="email", business_registration_number="123123123")
    ta_firm = TaFirm.objects.create(user=user_ta)
    user_ta.groups.add(group_ta)
    user_ta.groups.add(group_gym)
    user_ta.save()