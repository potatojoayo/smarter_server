from django.db import models

class TaFirm(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='ta_firm')

    class Meta:
        db_table = "ta_firms"