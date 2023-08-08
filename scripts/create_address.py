from authentication.models import User
from django.db.models import Count

from common.models import Address


def run():
    users = User.objects.annotate(num_addresses=Count('addresses')).filter(num_addresses=1, gym__isnull=False)
    for user in users:
        address = user.addresses.first()
        address.zip_code = user.gym.zip_code
        address.phone = user.phone
        address.save()
        # address = Address.objects.create(user=user, name='체육관', receiver=user.name, phone=user.phone,
        #                                  zip_code=user.gym.zip_code,
        #                                  address=user.gym.address, detail_address=user.gym.detail_address, default=True,
        #                                  is_active=True)
        print(address.address)
