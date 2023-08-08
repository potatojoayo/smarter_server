import pandas as pd
from django.db import transaction

from order.models import EasyOrder


@transaction.atomic()
def run():
    df = pd.read_csv('files/easy_orders.csv', keep_default_na=False, header=None)
    with transaction.atomic():
        for index, row in df.iterrows():
            id = row[0]
            user_id = row[1]
            contents = row[2]
            state = row[3]
            order_id = row[4]
            if not EasyOrder.objects.filter(pk=id).exists():
                easy_order = EasyOrder.objects.create(user_id=user_id, contents=contents, state=state, order_id=order_id)
                print(easy_order)


            

