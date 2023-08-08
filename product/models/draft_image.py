from django.db import models


class DraftImage(models.Model):

    image = models.ImageField(upload_to='member/logo')

