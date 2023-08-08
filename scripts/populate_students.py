import re
from datetime import datetime

from django.contrib.auth.models import Group
from django.db import transaction


from authentication.models import User
from business.models import  Gym
import pandas as pd

from gym_class.models import Level, ClassMaster
from gym_student.models import School, Student, Parent, Relationship


@transaction.atomic()
def run():

    path = 'files/students_youngam.csv'
    csv = pd.read_csv(filepath_or_buffer=path, skiprows=1)
    gym = Gym.objects.get(pk=3082)
    for row in csv.iterrows():
        series = row[1]

        student_name =  series.get(0)
        class_name = series.get(1)
        level_name = series.get(2)
        gender= series.get(3)
        if gender ==1:
            gender = '남자'
        else:
            gender = '여자'
        address = series.get(4)
        address_detail = series.get(5)
        school_name = series.get(6)
        if school_name =='':
            school_name = '스마터초등학교'
        price = series.get(8)
        sub_parent_name = series.get(9)
        sub_parent_phone = series.get(10)
        parent_name = series.get(11)
        if type(parent_name) == float:
            parent_name = '모름'

        print(parent_name)
        parent_phone = series.get(12)
        date_created = series.get(13)
        date_to_pay = series.get(14)
        student_birthday = str(series[15])
        splits = student_birthday.split('-')

        birthday = datetime(int(splits[0]), int(splits[1]), int(splits[2]))
        print(student_name, price, parent_name, date_to_pay, student_birthday)

        integers = re.findall(r'\d+', str(int(price)))
        price = int(''.join(integers))

        splits= student_birthday.split('-')

        month = splits[1].zfill(2)

        day = splits[2].zfill(2)

        month_day = month+day
        print(month + day)
        parent_phone = parent_phone.replace('-','')

        identification = parent_phone[3:] + month_day
        parent = Parent.objects.filter(user__phone=parent_phone)
        if parent.exists():
            parent  = parent.first()

        else:
            user = User.objects.create_user(identification=identification , name=parent_name, phone=parent_phone, password=month_day,)
            group = Group.objects.get(name="학부모")
            group.user_set.add(user)
            mom, _ = Relationship.objects.get_or_create(name='어머니')
            dad, _ = Relationship.objects.get_or_create(name='아버지')
            parent = Parent.objects.create(user=user, relationship=mom, address=address, detail_address=address_detail, supporter_name=sub_parent_name, supporter_relationship=dad, supporter_phone=sub_parent_phone )


        # relationship = models.ForeignKey(Relationship, on_delete=models.PROTECT, related_name="parent")
        # address = models.CharField(max_length=30, null=True, blank=True)
        # detail_address = models.CharField(max_length=150, null=True, blank=True)
        # zip_code = models.CharField(max_length=15, null=True, blank=True)
        # supporter_name = models.CharField(max_length=10, null=True, blank=True)
        # supporter_relationship = models.ForeignKey(Relationship, on_delete=models.PROTECT,
        #                                            related_name="supporter_parents", null=True, blank=True)
        # supporter_phone = models.CharField(max_length=20, null=True, blank=True)

        school, _ = School.objects.get_or_create(name=school_name,)

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
                                                date_entered=datetime.now(),
                                                gender=gender,
                                                day_to_pay=date_to_pay,
                                                price_to_pay=price)

        print(student)
