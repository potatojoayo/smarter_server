import pandas as pd
from django.db import transaction
from authentication.models import User
from business.models import Agency

def run():
    df = pd.read_csv('files/agencies.csv', keep_default_na=False, header=None)
    with transaction.atomic():
        for index, row in df.iterrows():
            identification = '0'+str(row[0])
            agency_name = row[1]
            address = row[2]
            region = row[3]
            user_name = row[4]
            phone = '0'+str(row[5])
            pwd = str(row[6])
            user = User.objects.create_user(identification=identification,name=user_name, phone=phone, password=pwd)
            agency = Agency.objects.create(user=user, region=region, name=agency_name, address=address)
            print(agency)

            

    
