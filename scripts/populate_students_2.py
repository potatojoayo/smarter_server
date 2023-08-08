import re
from datetime import datetime, timedelta

from django.contrib.auth.models import Group
from django.db import transaction


from authentication.models import User
from business.models import  Gym
import pandas as pd

from gym_class.models import Level, ClassMaster
from gym_student.models import School, Student, Parent, Relationship


@transaction.atomic()
def run():

    path = 'files/students.csv'
    csv = pd.read_csv(filepath_or_buffer=path, skiprows=0)
    gym = Gym.objects.get(pk=3134)
    for row in csv.iterrows():
        series = row[1]

        student_name =  series.get(0)
        print(student_name)

        class_name = (series.get(10))
        # class_name = '태권도반'
        level_name = (series.get(16))

        student_birthday = str(series[1])
        splits = student_birthday.split('.')
        birthday = datetime(int(splits[0]), int(splits[1]), int(splits[2]))
        month = splits[1].zfill(2)
        day = splits[2].zfill(2)
        month_day = month + day

        gender= series.get(2)
        if gender =='남':
            gender = '남자'
        else:
            gender = '여자'

        address = ''
        address_detail = ''

        school_name = ''

        date_to_pay = series.get(8)

        price = series.get(9)
        integers = re.findall(r'\d+', str(price))
        price = int(''.join(integers))

        sub_parent_name = ''
        sub_parent_phone = ''
        if sub_parent_name =='':
            sub_parent_name ='모름'
        if sub_parent_phone =='--':
            sub_parent_phone = ''

        parent_name = series.get(14)
        parent_phone = series.get(15)
        parent_phone = parent_phone.replace('-', '')

        identification = parent_phone[3:] + month_day

        parent = Parent.objects.filter(user__phone=parent_phone)

        if parent.exists():
            parent = parent.first()

        else:
            user = User.objects.create_user(identification=identification, name=parent_name, phone=parent_phone,
                                            password=month_day, )
            group = Group.objects.get(name="학부모")
            group.user_set.add(user)
            mom, _ = Relationship.objects.get_or_create(name='어머니')
            dad, _ = Relationship.objects.get_or_create(name='아버지')
            parent = Parent.objects.create(user=user, relationship=mom, address=address, detail_address=address_detail,
                                           supporter_name=sub_parent_name, supporter_relationship=dad,
                                           supporter_phone=sub_parent_phone)

        school, _ = School.objects.get_or_create(name=school_name, )

        level = Level.objects.filter(gym=gym, name=level_name)
        level = level.first()

        gym_class = ClassMaster.objects.get(gym=gym, name=class_name)

        student, _ = Student.objects.get_or_create(class_master=gym_class,
                                                   level=level,
                                                   parent=parent,
                                                   school=school,
                                                   name=student_name,
                                                   birthday=birthday,
                                                   status='수강중',
                                                   date_entered=datetime.now() -timedelta(days=1),
                                                   gender=gender,
                                                   day_to_pay=date_to_pay,
                                                   price_to_pay=price)

        print(student)
