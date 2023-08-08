from django.db import models

from cs.models.cs_request import CsRequest


class CsRequestContents(models.Model):
    cs_request = models.ForeignKey(CsRequest, on_delete=models.CASCADE, related_name='request_contents')
    contents = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, default=None)

    class Meta:
        db_table = 'cs_request_contents'