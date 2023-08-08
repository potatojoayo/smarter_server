from product.models import Draft


def run():
    draft = Draft.objects.get(user_id)