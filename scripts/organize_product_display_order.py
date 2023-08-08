from product.models import Category


def run():
    sub_categories = Category.objects.filter(parent__isnull=False)
    for sub_category in sub_categories:
        products = sub_category.sub_products.all().order_by('id')
        brands = []
        for product in products:
            if product.brand not in brands:
                brands.append(product.brand)

        for brand in brands:
            products = products.filter(brand=brand)

            print(sub_category.name, brand.name)
            for index, product in enumerate(products):
                product.display_order = index + 1
                product.save()
                print(product.name, product.display_order)

