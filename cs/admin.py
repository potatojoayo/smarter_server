from django.contrib import admin

from cs.models import CsRequest, CsRequestContents, CouponMaster, Coupon, CouponIssueHistory, CouponUseHistory, \
    CancelOrderRequest, ChangeRequest, ChangeRequestDetail, \
    CsPartialCancelHistory, ReturnRequest, ReturnRequestDetail, CouponMasterIssueHistory


# Register your models here.

@admin.register(CouponMasterIssueHistory)
class CouponMasterIssueHistoryAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'issued_count_per_gym',
                    'issued_amount_per_gym',
                    'total_issued_count',
                    'total_issued_amount',
                    'expired_day',
                    'coupon_message'
                    )

@admin.register(CsRequest)
class CsRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_requested')
    save_as = True


@admin.register(CsRequestContents)
class CsRequestContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'contents')

@admin.register(ChangeRequest)
class CsRequestChangeAdmin(admin.ModelAdmin):
    pass
@admin.register(ChangeRequestDetail)
class CsRequestChangeDetail(admin.ModelAdmin):
    pass


@admin.register(CsPartialCancelHistory)
class CsPartialCancelHistoryAdmin(admin.ModelAdmin):
    pass

@admin.register(CouponMaster)
class CouponMaster(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'date_created')
    save_as = True


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    save_as = True


@admin.register(CouponIssueHistory)
class CouponIssueHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'gym_name', 'date_issued')


@admin.register(CouponUseHistory)
class CouponUseHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'gym_name', 'date_used')


@admin.register(CancelOrderRequest)
class CancelOrderRequestAdmin(admin.ModelAdmin):
    search_fields = ('cs_request_number', 'order_number',)

@admin.register(ReturnRequest)
class CsRequestReturnAdmin(admin.ModelAdmin):
    list_display = ('id', 'cs_request')

@admin.register(ReturnRequestDetail)
class CsRequestReturnDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'cs_request_return')

