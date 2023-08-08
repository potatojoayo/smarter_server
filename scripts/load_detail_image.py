import pandas as pd
from django.core.files import File
from django.db import transaction

from product.models import Product, ProductMaster, Category, Brand

def run():
    sheets = pd.read_excel('files/products.xlsx', sheet_name=None, 
                           skiprows=[1, 2],
                           keep_default_na=False)
    with transaction.atomic():
        for sheet_name in sheets.keys():
            sheet = sheets[sheet_name]
            for index, row in sheet.iterrows():
                if row[0] and row[25]:
                    product_name = row[6]
                    thumbnail = row[22]
                    description_image = row[25]
                    parent_category = row[2]
                    '''
                    if '/' in description_image:
                        description_image = description_image.split('/')[0]
                    description_image = description_image.replace(',jpg','.jpg')
                    if '.jpg' not in description_image:
                        description_image += '.jpg'
                    '''

                    product_master = ProductMaster.objects.get(name=product_name)
                    print(product_name)
                    if thumbnail != '500image.jpg':
                        #try:
                        print(thumbnail)
                        product_master.thumbnail.save(thumbnail, File(open('files/상품/{}/대표이미지/{}'.format(parent_category, thumbnail.lower()), 'rb')))
                    else:
                        product_master.thumbnail.save('500image.jpg', File(open('files/500image.jpg','rb')))
                    if description_image != 'info-image.jpg':
                        product_master.description_image.save(description_image, File(open('files/상품/{}/상세이미지/{}'.format(parent_category, description_image.lower()), 'rb')))
                    else:
                        product_master.description_image.save(description_image, File(open('files/info-image.jpg', 'rb')))
                    print(product_master.name)


