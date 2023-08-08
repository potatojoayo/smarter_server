import pandas as pd
from django.db import transaction

from common.models import AddressZipCode
import numpy as np

@transaction.atomic()
def run():
    path = 'scripts/address_zip_code.csv'
    csv = pd.read_csv(filepath_or_buffer=path, encoding='cp949')
    csv = csv.replace({np.nan: None})
    AddressZipCode.objects.create(code='11', si_do="서울특별시", zip_code_start="1000", zip_code_end="8866")
    for row in csv.iterrows():
        series = row[1]
        code = series.get(0)
        si_do = series.get(1)
        si_gun_gu = series.get(2)
        zip_code_start = series.get(3)
        zip_code_end = series.get(4)
        parent = AddressZipCode.objects.filter(si_do=si_do)
        if parent.exists():
            parent = parent.first()
            AddressZipCode.objects.create(code=code,
                                          si_do=si_do,
                                          si_gun_gu=si_gun_gu,
                                          zip_code_start=zip_code_start,
                                          zip_code_end=zip_code_end,
                                          parent=parent)
        else:
            AddressZipCode.objects.create(code=code,
                                          si_do=si_do,
                                          si_gun_gu=si_gun_gu,
                                          zip_code_start=zip_code_start,
                                          zip_code_end=zip_code_end,
                                          parent=None)
