from django.db import models


class AddressZipCode(models.Model):

    code = models.CharField(max_length=5)
    si_do = models.CharField(max_length=10)
    si_gun_gu = models.CharField(max_length=20, null=True, blank=True)
    zip_code_start = models.CharField(max_length=5)
    zip_code_end = models.CharField(max_length=5)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def __str__(self):
        return "{}".format(self.si_do)
