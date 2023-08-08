import pandas as pd
from django.core.files import File
from django.db import transaction

from product.models import Product, ProductMaster, Category, Brand, ProductImage
from inventory.models import Supplier


def run():
    sheets = pd.read_excel('files/extra_products.xlsx', 
                           sheet_name=None, 
                           keep_default_na=False)
    product_number_surfix = 2000
    with transaction.atomic():
        for sheet_name in sheets.keys():
            sheet = sheets[sheet_name]
            for index, row in sheet.iterrows():
                print(row.iloc[0])
                if row.iloc[0]:
                    product_number = '{}{}'.format(row.iloc[0], product_number_surfix)
                    product_number_surfix += 1
                    model_number = row.iloc[1]
                    parent_category = row.iloc[2]
                    child_category = row.iloc[3]
                    brand = row.iloc[4]
                    supplier = row.iloc[5]
                    product_name = row.iloc[6]
                    need_draft = row.iloc[7]
                    price_consumer = row.iloc[8]
                    price_parent = row.iloc[9]
                    price_gym = row.iloc[10]
                    price_vendor = row.iloc[11]
                    color = row.iloc[12]
                    size = row.iloc[13]
                    price_additional = row.iloc[14] if row.iloc[14] else 0
                    price_delivery = row.iloc[15]
                    state = row.iloc[16]
                    delivery_type = row.iloc[17]
                    max_quantity_per_box = row.iloc[18] if row.iloc[18] else 0
                    inventory_quantity = row.iloc[19]
                    threshold_inventory_quantity = row.iloc[20] if row.iloc[20] else 0
                    goal_inventory_quantity = row.iloc[21] if row.iloc[21] else 0
                    thumbnail = row.iloc[22]
                    images = row.iloc[23]
                    description_image = row.iloc[24]


                    product_master_exists = ProductMaster.objects.filter(name=product_name).exists()
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

                        #product_master.thumbnail.save(thumbnail, File(open('files/상품/{}/대표이미지/{}'.format(p_category.name, thumbnail), 'rb')))
                        product_master.thumbnail.save('500image.jpg', File(open('files/500image.jpg','rb')))
                        print(thumbnail)

                        # product_master.description_image.save(description_image, File(open('files/images/{}'.format(description_image),'rb')))
                        # for image in images.split('/'):
                        #     if image == '':
                        #         continue
                        #     product_image = ProductImage.objects.create(product_master=product_master)
                        #     product_image.image.save(image, File(open('files/images/{}'.format(image),'rb')))
                    print(product_name)
                    product_master = ProductMaster.objects.get(name=product_name)


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

