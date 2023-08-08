from django.db import models


class Card(models.Model):

    company = models.CharField(max_length=20)
    number = models.CharField(max_length=50)
    installment_plan_months = models.IntegerField()
    is_interest_free = models.BooleanField()
    approve_no = models.CharField(max_length=20)
    use_card_point = models.BooleanField()
    card_type = models.CharField(max_length=10)
    owner_type = models.CharField(max_length=10)
    acquire_status = models.CharField(max_length=20)
    receipt_url = models.URLField()
    amount = models.IntegerField()

    def __str__(self):
        return self.company + ' - ' + self.number
