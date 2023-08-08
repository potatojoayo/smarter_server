from django.db import models


class ClassCardSuccess(models.Model):
    company = models.CharField(max_length=30)
    number = models.CharField(max_length=20)
    installmentPlanMonths = models.IntegerField()
    approveNo = models.CharField(max_length=10)
    cardType = models.CharField(max_length=10)
    ownerType = models.CharField(max_length=10)

    def __str__(self):
        return '{}. {}, {}, {}'.format(self.id, self.company,
                                       self.number, self.approveNo)
