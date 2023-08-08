import django.apps

from business.models import Business


def run():
    models = django.apps.apps.get_models()
    for model in models:
        if issubclass(model, Business):
            model.objects.all().update(email=None)

