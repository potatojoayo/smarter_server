from django.db import transaction


from authentication.models import User
from business.models import Subcontractor
from common.models import Membership, ExtraPriceDelivery
import pandas as pd
from order.models import ZipCode
from django.contrib.auth.models import Group


def run():
    Group.objects.create(name='학부모')
    Group.objects.create(name='체육관')
    Group.objects.create(name='체육사')
    Group.objects.create(name='작업실')
    Group.objects.create(name='관리자')
    Group.objects.create(name='로고시안팀')
    Group.objects.create(name='배송관리팀')
    super_user = User.objects.create_superuser(name='superuser', phone='01000000000', identification='admin', password='admin')
    group = Group.objects.get(name='관리자')
    super_user.groups.add(group)
    super_user.save()
    delivery = User.objects.create_user(identification='delivery', name='delivery', phone='01011111111', password='delivery')
    group = Group.objects.get(name='배송관리팀')
    delivery.groups.add(group)
    delivery.save()
    group = Group.objects.get(name='로고시안팀')
    logoa = User.objects.create_user(identification='logoa', name='logoa', phone='01022222222',
                                     password='logoa')
    logob = User.objects.create_user(identification='logob', name='logob', phone='01033333333',
                                     password='logob')
    belt = User.objects.create_user(identification='belt', name='belt', phone='01044444444',
                                     password='belt')
    prework = User.objects.create_user(identification='prework', name='prework', phone='01055555555',
                                     password='prework')
    outwork = User.objects.create_user(identification='outwork', name='outwork', phone='01066666666',
                                     password='outwork')
    logoa.groups.add(group)
    Subcontractor.objects.create(user=logoa, name="로고작업실A")
    logoa.save()

    logob.groups.add(group)
    Subcontractor.objects.create(user=logob, name="로고작업실B")
    logob.save()

    belt.groups.add(group)
    Subcontractor.objects.create(user=belt, name="띠자수작업실")
    belt.save()

    prework.groups.add(group)
    Subcontractor.objects.create(user=prework, name="전처리작업실", is_pre_working=True)
    prework.save()

    outwork.groups.add(group)
    Subcontractor.objects.create(user=outwork, name="외부작업실", is_out_working=True)
    outwork.save()

    Membership.objects.create(name='일반회원')
    Membership.objects.create(name='우수회원')
    Membership.objects.create(name='최우수회원')
    ExtraPriceDelivery.objects.create(price=3000)

    #zip_code db에 넣기
    path = 'files/zip_code.xlsx'
    sheets = pd.read_excel(path, sheet_name='제주&도서산간지역 (중복제거)', usecols='A:D', keep_default_na=False)
    with transaction.atomic():
        for row in sheets.itertuples():
            ZipCode.objects.create(address=row.address, zip_code=row.zip_code, additional_delivery_price=row.cost)


