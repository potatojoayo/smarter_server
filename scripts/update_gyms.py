import pandas as pd
from django.db import transaction
from authentication.models import User
from business.models import Agency, Gym

def run():
    df = pd.read_csv('files/gyms.csv', keep_default_na=False, header=None)
    with transaction.atomic():
        for index, row in df.iterrows():
            business_registration_number = None
            gym_name = row[3]
            try:
                gym = Gym.objects.get(name=gym_name)
            except:
                continue
            if row[5]:
                business_registration_number = str(row[5])+str(row[6])+str(row[7]).zfill(5)
            print(gym_name)
            print(business_registration_number)
            gym.business_registration_number = business_registration_number
            gym.save()
            

    
