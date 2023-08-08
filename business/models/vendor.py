from django.db import models

from business.models.business import Business


class Vendor(Business):

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='vendor')
