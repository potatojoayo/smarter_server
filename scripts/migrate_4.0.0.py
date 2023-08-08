from django.db import transaction

from .change_draft import run as change_draft
from .calculate_gym_purchased_amount import run as calculate_gym_purchased_amount
from .load_address_zip_code import run as address_zip_code
from .initial_coupon_master import run as initial_coupon_master

@transaction.atomic()
def run():
    change_draft()
    calculate_gym_purchased_amount()
    address_zip_code()
    initial_coupon_master()


