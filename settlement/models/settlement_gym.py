from django.db import models

from settlement.models.settlement import Settlement
from business.models.gym import Gym


class SettlementGym(Settlement):

    gym = models.ForeignKey(Gym, on_delete=models.PROTECT)
