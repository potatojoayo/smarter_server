from django.db import models

from product.models import NewDraft


class DraftSize(models.Model):
    new_draft = models.ForeignKey(NewDraft, on_delete=models.CASCADE, related_name='sizes')
    name = models.CharField(max_length=50)

    back_width = models.IntegerField(default=0)
    back_height = models.IntegerField(default=0)
    left_chest_width = models.IntegerField(default=0)
    left_chest_height = models.IntegerField(default=0)
    right_chest_width = models.IntegerField(default=0)
    right_chest_height = models.IntegerField(default=0)
    left_shoulder_width = models.IntegerField(default=0)
    left_shoulder_height = models.IntegerField(default=0)
    right_shoulder_width = models.IntegerField(default=0)
    right_shoulder_height = models.IntegerField(default=0)
    heap_width = models.IntegerField(default=0)
    heap_height = models.IntegerField(default=0)
    left_pant_middle_width = models.IntegerField(default=0)
    left_pant_middle_height = models.IntegerField(default=0)
    right_pant_middle_width = models.IntegerField(default=0)
    right_pant_middle_height = models.IntegerField(default=0)
    left_pant_low_width = models.IntegerField(default=0)
    left_pant_low_height = models.IntegerField(default=0)
    right_pant_low_width = models.IntegerField(default=0)
    right_pant_low_height = models.IntegerField(default=0)
    flag_width = models.IntegerField(default=0)
    flag_height = models.IntegerField(default=0)

    def __str__(self):
        return self.name


