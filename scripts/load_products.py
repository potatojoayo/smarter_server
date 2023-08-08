import pandas as pd
from django.core.files import File
from django.db import transaction

from product.models import Product, ProductMaster, Category, Brand, ProductImage
from inventory.models import Supplier


def run():
    sheets = pd.read_excel('files/products.xlsx', sheet_name=None, 
                           skiprows=[1, 2],
                           keep_default_na=False)
    product_number_surfix = 0
    with transaction.atomic():
        for sheet_name in sheets.keys():
            sheet = sheets[sheet_name]
            for index, row in sheet.iterrows():
                if row[0]:
                    product_number = '{}{}'.format(row[0], product_number_surfix)
                    product_number_surfix += 1
                    model_number = row[1]
                    parent_category = row[2]
                    child_category = row[3]
                    brand = row[4]
                    supplier = row[5]
                    product_name = row[6]
                    need_draft = row[7]
                    price_consumer = row[8]
                    price_parent = row[9]
                    price_gym = row[10]
                    price_vendor = row[11]
                    color = row[12]
                    size = row[13]
                    price_additional = row[14] if row[14] else 0
                    price_delivery = row[15]
                    state = row[16]
                    delivery_type = row[17]
                    max_quantity_per_box = row[18] if row[18] else 0
                    inventory_quantity = row[19]
                    threshold_inventory_quantity = row[20] if row[20] else 0
                    goal_inventory_quantity = row[21] if row[21] else 0
                    thumbnail = row[22]
                    images = row[23]
                    description_image = row[25]


                    product_master_exists = ProductMaster.objects.filter(name=product_name, sub_category__name=child_category).exists()
                    if not product_master_exists:

                        # 카테고리 가져오거나 생성
                        p_category_exists = Category.objects.filter(name=parent_category, depth=0).exists()
                        if p_category_exists:
                            p_category = Category.objects.get(name=parent_category, depth=0)
                        else:
                            last = Category.objects.all().order_by('-order').first()
                            if last:
                                p_category = Category.objects.create(name=parent_category,
                                                                     order=last.order + 1,
                                                                     depth=0
                                                                     )
                            else:
                                p_category = Category.objects.create(name=parent_category,
                                                                     order=0,
                                                                     depth=0
                                                                     )

                        c_category_exists = Category.objects.filter(name=child_category, depth=1).exists()
                        if c_category_exists:
                            c_category = Category.objects.get(name=child_category, depth=1)
                        else:
                            last = Category.objects.filter(parent=p_category).order_by('-order').first()
                            if last:
                                c_category = Category.objects.create(name=child_category,
                                                                 order=last.order + 1,
                                                                 depth=1,
                                                                 parent=p_category
                                                                 )
                            else:
                                c_category = Category.objects.create(name=child_category,
                                                                     order=0,
                                                                     depth=1,
                                                                     parent=p_category
                                                                     )


                        # 브랜드 가져오거나 생성
                        brand_exists = Brand.objects.filter(name=brand).exists()
                        if brand_exists:
                            brand_instance = Brand.objects.get(name=brand)
                        else:
                            last = Brand.objects.all().order_by('-order')
                            if last.count() > 0:
                                last = last.first()
                                brand_instance = Brand.objects.create(name=brand, order=last.order + 1)
                            else:
                                brand_instance = Brand.objects.create(name=brand, order=0)

                        supplier, created = Supplier.objects.get_or_create(name=supplier)

                        product_master = ProductMaster.objects.create(product_number=product_number,
                                                                      category=p_category,
                                                                      sub_category=c_category,
                                                                      brand=brand_instance,
                                                                      supplier=supplier,
                                                                      name=product_name,
                                                                      need_draft=need_draft,
                                                                      price_consumer=price_consumer,
                                                                      price_parent=price_parent,
                                                                      price_gym=price_gym,
                                                                      price_vendor=price_vendor,
                                                                      price_delivery=price_delivery,
                                                                      state=state,
                                                                      delivery_type=delivery_type,
                                                                      max_quantity_per_box=max_quantity_per_box if max_quantity_per_box else None,
                                                                      threshold_inventory_quantity=threshold_inventory_quantity,
                                                                      goal_inventory_quantity=goal_inventory_quantity,
                                                                      )

                        if thumbnail != '500image.jpg':
                            #try:
                            product_master.thumbnail.save(thumbnail, File(open('files/상품/{}/대표이미지/{}'.format(parent_category, thumbnail.lower()), 'rb')))
                        else:
                            product_master.thumbnail.save('500image.jpg', File(open('files/500image.jpg','rb')))
                        if description_image != 'info-image.jpg':
                            product_master.description_image.save(description_image, File(open('files/상품/{}/상세이미지/{}'.format(parent_category, description_image.lower()), 'rb')))
                        else:
                            product_master.description_image.save(description_image, File(open('files/info-image.jpg', 'rb')))

                        # for image in images.split('/'):
                        #     if image == '':
                        #         continue
                        #     product_image = ProductImage.objects.create(product_master=product_master)
                        #     product_image.image.save(image, File(open('files/images/{}'.format(image),'rb')))

                    product_master = ProductMaster.objects.get(name=product_name, sub_category__name=child_category)


                    print(product_master)

                    product = Product.objects.create(
                        product_master=product_master,
                        name=product_name,
                        model_number=model_number,
                        color=color,
                        size=size,
                        price_additional=price_additional if price_additional else 0,
                        state=state,
                        inventory_quantity=inventory_quantity,
                        threshold_inventory_quantity=product_master.threshold_inventory_quantity,
                        goal_inventory_quantity=product_master.goal_inventory_quantity,
                        expected_inventory_quantity=0,
                        lack_inventory=False
                    )
                    print(product)

