import pandas as pd
from django.db import transaction
from authentication.models import User
from business.models import Agency, Gym

def run():
    df = pd.read_csv('files/gyms.csv', keep_default_na=False, header=None)
    with transaction.atomic():
        for index, row in df.iterrows():
            identification = '0'+str(row[0])
            pwd = str(row[1])
            is_active = row[2]
            gym_name = row[3]
            user_name = row[4]
            if '외1명' in user_name:
                user_name = user_name[:3]
            print(user_name)
            business_registration_number = ''
            if row[5]:
                business_registration_number = str(row[5]).zfill(3)+str(row[6]).zfill(2)+str(row[7]).zfill(5)
            zip_code = row[8]
            email = row[9]
            address = row[10]
            detail_address = row[11]
            agency_name = row[12]
            phone = str(row[13])
            phone = phone.strip()
            email = row[14]

            if Gym.objects.filter(name=gym_name).exists():
                continue

            users = User.objects.filter(identification=identification)
            if users.count() > 0:
                user = users.first()
                user.phone = phone 
                user.set_password(pwd)
                print(agency_name)
                agency = None
                if agency_name:
                    agency = Agency.objects.get(name=agency_name)
                print(business_registration_number)
                user.gym.agency = agency
                user.business_registration_number = business_registration_number
                user.email = email
                user.save()
            else:
                try:
                    user = User.objects.get(identification=identification)
                except:
                    user = User.objects.create_user(identification=identification,name=user_name, phone=phone, password=pwd)
                print(agency_name)
                agency = None
                if agency_name:
                    agency = Agency.objects.get(name=agency_name)
                gym = Gym.objects.create(user=user, name=gym_name, address=address, detail_address=detail_address, zip_code=zip_code, email=email, business_registration_number=business_registration_number, agency=agency)
                print(gym)

                

        
