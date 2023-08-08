from datetime import datetime, timedelta

import graphene
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import Group
from django.db import transaction

from authentication.models import User
from class_payment.models import ClassPaymentMaster
from gym_class.models import AttendanceMaster, AttendanceDetail
from gym_student.methods.create_class_payment import create_class_payment
from gym_student.methods.send_notification_installation import send_notification_installation
from gym_student.methods.update_day_to_pay import update_day_to_pay
from gym_student.models import Parent, Student, Relationship, School
from gym_student.types.parent_input_type import ParentInputType
from gym_student.types.student.student_input_type import StudentInputType


class CreateStudent(graphene.Mutation):
    class Arguments:
        student = StudentInputType()
        parent = ParentInputType()

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info, parent, student):
        user = info.context.user
        gym = info.context.user.gym
        if parent.id:
            parent_object = Parent.objects.get(pk=parent.id)
            relationship, _ = Relationship.objects.get_or_create(name=parent.relationship_name)
            user = parent_object.user
            user.name = parent.name
            user.save()
            parent_object.relationship = relationship
            parent_object.address = parent.address
            parent_object.detail_address = parent.detail_address
            parent_object.zip_code = parent.zip_code
            parent_object.save()
            Parent.objects.filter(pk=parent.id).update(
                relationship=relationship,
                address=parent.address,
                detail_address=parent.detail_address,
                zip_code=parent.zip_code, )
            if parent.supporter_name:
                supporter_relationship, _ = Relationship.objects.get_or_create(name=parent.supporter_relationship)
                parent_object.supporter_relationship = supporter_relationship
                parent_object.supporter_name = parent.supporter_name
                parent_object.supporter_phone = parent.supporter_phone
                parent_object.save()
        else:
            pwd = str(student.birthday.month).zfill(2) + str(student.birthday.day).zfill(2)
            relationship, _ = Relationship.objects.get_or_create(name=parent.relationship_name)
            user_parent = User.objects.create_user(name=parent.name,
                                                   phone=parent.phone,
                                                   identification=parent.phone[3:] + pwd,
                                                   password=pwd)
            group = Group.objects.get(name="학부모")
            user_parent.groups.add(group)
            user_parent.save()
            parent_object = Parent.objects.create(user=user_parent,
                                                  relationship=relationship,
                                                  address=parent.address,
                                                  detail_address=parent.detail_address,
                                                  zip_code=parent.zip_code,
                                                  )

            if parent.supporter_name:
                supporter_relationship, _ = Relationship.objects.get_or_create(name=parent.supporter_relationship)
                parent_object.supporter_relationship = supporter_relationship
                parent_object.supporter_name = parent.supporter_name
                parent_object.supporter_phone = parent.supporter_phone
                parent_object.save()
            send_notification_installation(phone_number=parent.phone, gym_id=gym.id)
        class_master = gym.class_masters.get(name=student.class_name)
        level = gym.levels.get(name=student.level_name)
        schools = School.objects.filter(name=student.school_name)
        if schools :
            school = School.objects.filter(name=student.school_name).first()
        else:
            school = School.objects.create(name=student.school_name)
        # school, _ = School.objects.get_or_create(name=student.school_name)
        if not student.id:
            print('not student id')
            print(student.class_date_start)
            s = Student.objects.create(parent=parent_object,
                                       class_master=class_master,
                                       level=level,
                                       school=school,
                                       name=student.name,
                                       birthday=student.birthday,
                                       status=student.status,
                                       phone=student.phone,
                                       height=student.height,
                                       weight=student.weight,
                                       date_entered=student.date_entered,
                                       day_to_pay=student.day_to_pay,
                                       gender=student.gender,
                                       price_to_pay=student.price_to_pay,
                                       memo_for_health = student.memo_for_health,
                                       memo_for_price = student.memo_for_price,
                                       memo = student.memo,
                                       class_date_start=student.class_date_start
                                       )
            class_master = s.class_master
            now = datetime.now()
            today = now.weekday()
            today_detail = class_master.class_details.filter(day=today, is_deleted=False)

            if today_detail.exists() and s.date_entered <= now.date() :
                class_detail = today_detail.first()
                attendance_master, created = AttendanceMaster.objects.get_or_create(
                    class_master=class_master,
                    class_detail=class_detail,
                    gym=gym,
                    date=datetime(year=now.year,month=now.month, day=now.day)
                )

                AttendanceDetail.objects.create(student=s,
                                                attendance_master=attendance_master
                                                )
            ClassPaymentMaster.objects.filter(student=s,
                                              date_to_pay__gte=datetime.today(),
                                              payment_status='미납'
                                              ).delete()
            print(s)
            print(s.class_date_start)
            if now.date() + relativedelta(months=1) + timedelta(days=-1) > s.class_date_start:
                create_class_payment(student=s)

        else:
            s = Student.objects.get(pk=student.id)
            old_class_master = s.class_master
            new_class_master = class_master
            changing_class_master = False
            if old_class_master != new_class_master:
                changing_class_master = True

            old_day_to_pay = s.day_to_pay
            new_day_to_pay = student.day_to_pay
            changing_day_to_pay = False
            if old_day_to_pay != new_day_to_pay:
                changing_day_to_pay = True
            print('112232')
            print(student.class_date_start)
            Student.objects.filter(pk=student.id).update(parent=parent_object,
                                                         class_master_id=new_class_master,
                                                         level=level,
                                                         school=school,
                                                         name=student.name,
                                                         birthday=student.birthday,
                                                         status=student.status,
                                                         phone=student.phone,
                                                         height=student.height,
                                                         weight=student.weight,
                                                         date_entered=student.date_entered,
                                                         day_to_pay=student.day_to_pay,
                                                         gender=student.gender,
                                                         price_to_pay=student.price_to_pay,
                                                         memo_for_health=student.memo_for_health,
                                                         memo_for_price=student.memo_for_price,
                                                         memo=student.memo,
                                                         class_date_start=student.class_date_start)
            if changing_class_master:
                attendance_masters = AttendanceMaster.objects.filter(class_master=old_class_master,
                                                                     date__gte=datetime.today()
                                                                     )
                if attendance_masters.exists():
                    attendance_master = attendance_masters.first()
                    attendance_details = AttendanceDetail.objects.filter(student=s,
                                                                         attendance_master=attendance_master,
                                                                         )
                    attendance_details.delete()
                now = datetime.now()
                today = now.weekday()
                today_detail = new_class_master.class_details.filter(day=today)
                if today_detail.exists():
                    class_detail = today_detail.first()
                    attendance_master, created = AttendanceMaster.objects.get_or_create(class_master=new_class_master,
                                                                                        class_detail=class_detail,
                                                                                        date__gte=datetime(year=now.year,
                                                                                        month=now.month,
                                                                                        day=now.day
                                                                                        ))
                    AttendanceDetail.objects.create(student=s,
                                                    attendance_master=attendance_master
                                                    )

            # if changing_day_to_pay:
            #     student = Student.objects.get(pk=student.id)
            #     update_day_to_pay(student=student, new_day_to_pay=new_day_to_pay, old_day_to_pay=old_day_to_pay)
            #     # now = datetime.now()
            #     # if (now + relativedelta(days=7)) >= datetime(year=now.year, month=now.month, day=new_day_to_pay):
            #     #     ex_class_date_from = now + relativedelta(months=-1)
            #     #     order_id = 'C{}'.format(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
            #     #     date_to_pay = datetime(year=now.year, month=now.month, day=new_day_to_pay)
            #     #     pay_date = date_to_pay if date_to_pay > now else date_to_pay + relativedelta(months=1)
            #     #     pay_date_from = pay_date
            #     #     pay_date_to = pay_date_from + relativedelta(months=1) + timedelta(days=-1)
            #     #     ClassPaymentMaster.objects.get_or_create(class_master=s.class_master,
            #     #                                              order_id=order_id,
            #     #                                              class_name=s.class_master.name,
            #     #                                              student=s,
            #     #                                              price=s.price_to_pay,
            #     #                                              date_from=pay_date_from,
            #     #                                              date_to=pay_date_to,
            #     #                                              price_to_pay=s.price_to_pay,
            #     #                                              date_to_pay=pay_date)

        return CreateStudent(success=True)
