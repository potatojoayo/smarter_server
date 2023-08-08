from datetime import datetime
from django.db.models import Q
import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from fields import OrderedDjangoFilterConnectionField
from order.models import OrderDetail
from .fields.draft_request_field import DraftRequestField
from .fields.recent_ordered_products_field import RecentOrderedProductsField
from .models import Category, Brand, ProductMaster, DraftRequest, Product, NewDraft

from .models import Category, Brand, Draft

from .mutations import CreateOrUpdateProductMaster
from .mutations.change_color import ChangeColor
from .mutations.change_display_order import ChangeDisplayOrder
from .mutations.change_size import ChangeSize
from .mutations.create_draft import CreateDraft
from .mutations.create_draft_request import CreateDraftRequest
from .mutations.create_multiple_drafts import CreateMultipleDrafts
from .mutations.create_new_draft import CreateNewDraft
from .mutations.create_or_update_draft import CreateOrUpdateDraft
from .mutations.delete_color import DeleteColor
from .mutations.delete_drafts import DeleteDrafts
from .mutations.delete_multiple_drafts import DeleteMultipleDrafts
from .mutations.delete_size import DeleteSize
from .mutations.finish_draft_request import FinishDraftRequest
from .mutations.update_brand_mutation import UpdateBrand
from .mutations.update_category_mutation import UpdateCategory
from .mutations.complete_draft_request import CompleteDraftRequest 
from product.types.brand.brand_type import BrandType
from product.types.category.category_type import CategoryType
from product.types.product_master.product_master_node import ProductMasterNode
from product.types.draft_request.draft_request_node import DraftRequestNode

from product.types.product_master.product_master_type import ProductMasterType
from .mutations.update_draft_image import UpdateDraftImage
from .mutations.update_drafts import UpdateDrafts
from .mutations.update_new_draft import UpdateNewDraft
from .mutations.update_product_master_memo import UpdateProductMasterMemo

from .types.draft.draft_type import DraftType
from .types.draft.new_draft_type import NewDraftType
from .types.product.product_node import ProductNode
from .types.product.product_type import ProductType
from .types.product.products_type import ProductMastersType


class Query(graphene.ObjectType):

    categories = graphene.List(CategoryType, depth=graphene.Int(), parent=graphene.Int())
    brands = graphene.List(BrandType, category=graphene.String())
    draft = graphene.Field(NewDraftType, id=graphene.Int(required=True))
    recent_ordered_products = RecentOrderedProductsField(ProductMasterNode)
    product_master = graphene.Field(ProductMasterType, id=graphene.Int())
    product_master_node = relay.Node.Field(ProductMasterNode)
    product_masters = OrderedDjangoFilterConnectionField(ProductMasterNode, orderBy=graphene.String())
    products = OrderedDjangoFilterConnectionField(ProductNode, orderBy=graphene.String())
    product_list = graphene.List(ProductType, product_master_id=graphene.Int(), product_name=graphene.String())
    product_master_list = graphene.List(ProductMasterType, brand=graphene.String(), sub_category=graphene.String())
    drafts = graphene.List(NewDraftType, user_id=graphene.Int(), sub_category_name=graphene.String())
    today_draft_request_count_by_state = graphene.Int(state=graphene.String())
    draft_request = relay.Node.Field(DraftRequestNode)
    draft_requests = DraftRequestField(DraftRequestNode, keyword=graphene.String())
    brand_list = graphene.List(graphene.String, sub_category=graphene.String())
    date_range = graphene.List(graphene.Date)

    my_drafts = graphene.List(NewDraftType, sub_category_name=graphene.String())
    @staticmethod
    def resolve_my_drafts(_, info, sub_category_name=None):
        user = info.context.user
        if sub_category_name:
            return user.new_drafts.filter(sub_category__name=sub_category_name)
        return user.new_drafts.all()


    cs_product_masters = graphene.Field(ProductMastersType, category=graphene.String(),
                                        sub_category=graphene.String(),
                                        brand=graphene.String(),
                                        state=graphene.String(),
                                        page=graphene.Int())

    @staticmethod
    def resolve_cs_product_masters(_, __, page, **kwargs):
        category = kwargs.get('category')
        sub_category = kwargs.get('sub_category')
        brand = kwargs.get('brand')
        state = kwargs.get('state')
        q = Q()
        if category and category != '전체':
            q.add(Q(category__name=category), q.AND)
        if sub_category and sub_category != '전체':
            q.add(Q(sub_category__name=sub_category), q.AND)
        if state and state != '전체':
            q.add(Q(state=state), q.AND)
        if brand and brand != '전체':
            q.add(Q(brand__name=brand), q.AND)
        product_masters = ProductMaster.objects.filter(q).order_by('-date_created')
        return ProductMastersType(
            product_masters=product_masters[10 * (page - 1):10 * page],
            total_count=product_masters.count()
        )

    @staticmethod
    def resolve_product_list(_, __, product_master_id=None, product_name=None):
        if product_master_id:
            return Product.objects.filter(product_master_id=product_master_id, state='판매중', is_deleted=False).order_by('id')
        elif product_name:
            return Product.objects.filter(name=product_name, state='판매중', is_deleted=False).order_by('id')


    @staticmethod
    def resolve_product_master_list(_, __, brand, sub_category):
        if brand and sub_category:
            return ProductMaster.objects.filter(brand__name=brand, sub_category__name=sub_category, state='판매중')

    @staticmethod
    def resolve_draft(_, __, id):
        return NewDraft.objects.get(pk=id)

    @staticmethod
    def resolve_today_draft_request_count_by_state(_, __, state):
        if state == '전체':
            return DraftRequest.objects.all().distinct().count()
        return DraftRequest.objects.filter(
            state=state,
        ).distinct().count()

    @staticmethod
    def resolve_product_master(_, __, id):
        return ProductMaster.objects.get(pk=id)

    @staticmethod
    def resolve_categories(root, info, depth=None, parent=None):
        return Category.objects.filter(depth=depth if depth else 0, parent_id=parent).order_by('order')

    @staticmethod
    def resolve_brands(_, __, category=None):
        print(category)
        if category:
            return Brand.objects.filter(products__sub_category__name=category).distinct()
        return Brand.objects.all()

    @staticmethod
    def resolve_drafts(_, __, user_id,  sub_category_name=None):
        print(user_id, sub_category_name)
        if sub_category_name:
            return NewDraft.objects.filter(user_id=user_id, sub_category__name=sub_category_name)
        return NewDraft.objects.filter(user_id=user_id, is_deleted=False,)


    @staticmethod
    def resolve_brand_list(_, __, sub_category):
        brand_list = []
        product_masters = ProductMaster.objects.filter(sub_category__name=sub_category)
        for product_master in product_masters:
            brand_list.append(product_master.brand)

        brand_list = list(set(brand_list))

        return brand_list


class Mutation(graphene.ObjectType):
    update_brand = UpdateBrand.Field()
    update_category = UpdateCategory.Field()
    create_or_update_product_master = CreateOrUpdateProductMaster.Field()
    create_or_update_draft = CreateOrUpdateDraft.Field()
    create_draft_request = CreateDraftRequest.Field()
    complete_draft_request = CompleteDraftRequest.Field()
    update_drafts = UpdateDrafts.Field()
    create_draft = CreateDraft.Field()
    create_multiple_drafts = CreateMultipleDrafts.Field()
    delete_drafts = DeleteDrafts.Field()
    delete_multiple_drafts = DeleteMultipleDrafts.Field()
    update_draft_image = UpdateDraftImage.Field()
    update_new_draft = UpdateNewDraft.Field()
    change_color = ChangeColor.Field()
    change_size = ChangeSize.Field()
    delete_color = DeleteColor.Field()
    delete_size = DeleteSize.Field()
    change_display_order = ChangeDisplayOrder.Field()
    create_new_draft = CreateNewDraft.Field()
    finish_draft_request = FinishDraftRequest.Field()
    update_product_master_memo = UpdateProductMasterMemo.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


