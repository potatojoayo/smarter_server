from django.db import models

from settlement.models.settlement import Settlement
from business.models.agency import Agency


class SettlementAgency(Settlement):

    agency = models.ForeignKey(Agency, on_delete=models.PROTECT)
