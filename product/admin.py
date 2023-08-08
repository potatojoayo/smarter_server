from django.contrib import admin

from .models import CategoryImage, Draft, DraftRequest, DraftImage, NewDraft, DraftSize
from .models.product import Product
from .models.product_master import ProductMaster
from .models.category import Category
from .models.brand import Brand
from .models.color import Color
from .models.product_image import ProductImage


@admin.register(DraftImage)
class DraftImageAdmin(admin.ModelAdmin):
    pass


@admin.register(DraftRequest)
class DraftRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(Draft)
class DraftAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_master', 'price_work', 'price_work_labor')
    search_fields = ('user__gym__name', 'product_master__name')

@admin.register(NewDraft)
class NewDraftAdmin(admin.ModelAdmin):
    list_display = ('user', 'sub_category', 'price_work', 'price_work_labor')
    search_fields = ('user__gym__name', 'sub_category__name')

@admin.register(ProductMaster)
class ProductMasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'delivery_type', 'state', 'date_created')
    search_fields = ('name', 'category__name', 'sub_category__name', 'brand__name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'order', 'depth')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('order','name')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass



@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'size', 'color')
    search_fields = ['name']


@admin.register(DraftSize)
class DraftSizeAdmin(admin.ModelAdmin):
    list_display = ('id',)
