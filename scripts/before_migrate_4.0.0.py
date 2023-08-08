from django.db import transaction
from .email_none import run as email_none


@transaction.atomic()
def run():
    email_none()

