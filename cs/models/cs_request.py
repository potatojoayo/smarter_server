from django.db import models

from business.models import Gym
from order.models import OrderMaster


class CsRequest(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='cs_requests')
    order_master = models.ForeignKey(OrderMaster, on_delete=models.CASCADE, related_name='cs_requests', null=True, blank=True)
    request_number = models.CharField(max_length=20)
    category = models.CharField(max_length=15, default='일반문의')
    order_number = models.CharField(max_length=20, null=True, blank=True)
    order_state = models.CharField(max_length=20, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    reason = models.CharField(max_length=100, null=True, blank=True)
    cs_state = models.CharField(max_length=20, default='미처리')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'cs_requests'

    def __str__(self):
        return 'id:'+str(self.gym.user.id)+str(self.gym.user.name)+"님의 문의사항"