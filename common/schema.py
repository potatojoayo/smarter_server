import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from authentication.models import User
from business.models import Gym
from common.mutations.create_or_update_address import CreateOrUpdateAddress
from common.mutations.create_or_update_faq import CreateOrUpdateFaq
from common.mutations.delete_address import DeleteAddress
from common.mutations.delete_faq import DeleteFaq
from common.mutations.read_notification import ReadNotification
from common.types import NoticeNode
from common.mutations.create_or_update_additional_delivery_price import CreateOrUpdateAdditionalDeliveryPrice
from common.mutations.create_or_update_delivery_agency import CreateOrUpdateDeliveryAgency
from common.mutations.create_or_update_bank_account import CreateOrUpdateBankAccount
from common.mutations.create_or_update_banner import CreateOrUpdateBanner
from common.mutations.create_or_update_noitce import CreateOrUpdateNoice
from common.mutations.delete_info_bank_account import DeleteInfoBankAccount
from common.mutations.delete_delivery_agency import DeleteDeliveryAgency
from common.mutations.delete_notice import DeleteNotice
from common.mutations.update_extra_price_delivery import UpdateExtraPriceDelivery
from common.mutations.update_membership import UpdateMembership
from common.types import AddressType
from common.types.address_zip_code_type import AddressZipCodeType
from common.types.bank_account_type import BankAccountType
from common.types.banner_type import BannerType
from common.types.delivery_agency_type import DeliveryAgencyType
from common.types.extra_price_delivery_type import ExtraPriceDeliveryType
from common.types.faq_node import FaqNode
from common.types.membership_type import MembershipType
from common.types.notification_node import NotificationNode
from common.models import Notification, DeliveryAgency, Membership, Banner, BankAccount, ExtraPriceDelivery, Notice, \
    AddressZipCode
from fields.user_filtered_django_filter_connection_field import UserFilteredDjangoFilterConnectionField
from common.mutations import ReadNotifications


class Query(graphene.ObjectType):

    address_zip_codes = graphene.List(AddressZipCodeType)

    @staticmethod
    def resolve_address_zip_codes(_, __):
        return AddressZipCode.objects.filter(parent__isnull=True)

    # my_notifications = graphene.List(NotificationType)
    my_notifications = UserFilteredDjangoFilterConnectionField(NotificationNode, orderBy=graphene.String())
    count_new_notifications = graphene.Int()
    delivery_agencies = graphene.List(DeliveryAgencyType)

    my_addresses = graphene.List(AddressType)
    addresses = graphene.List(AddressType, user_id=graphene.Int())

    @staticmethod
    def resolve_addresses(_, __, user_id):
        user = User.objects.get(pk=user_id)
        return user.addresses.filter(is_deleted=False)

    notification_node = relay.Node.Field(NotificationNode)
    notifications = DjangoFilterConnectionField(NotificationNode)

    notices = DjangoFilterConnectionField(NoticeNode)

    faqs = DjangoFilterConnectionField(FaqNode)

    memberships = graphene.List(MembershipType)

    banners = graphene.List(BannerType)

    bank_accounts = graphene.List(BankAccountType)
    default_bank_account = graphene.Field(BankAccountType)

    extra_price_delivery = graphene.Field(ExtraPriceDeliveryType)

    @staticmethod
    def resolve_default_bank_account(_, __):
        return BankAccount.objects.get(is_default=True)

    @staticmethod
    def resolve_my_addresses(_, info):
        return info.context.user.addresses.filter(is_deleted=False)

    @staticmethod
    def resolve_extra_price_delivery(_, __):
        return ExtraPriceDelivery.objects.all().first()

    @staticmethod
    def resolve_bank_accounts(_, __):
        return BankAccount.objects.all()

    @staticmethod
    def resolve_banners(_, __):
        return Banner.objects.all()

    @staticmethod
    def resolve_memberships(_, __):
        return Membership.objects.all()

    @staticmethod
    def resolve_count_new_notifications(_, info):
        return Notification.objects.filter(user=info.context.user, date_read__isnull=True).count()

    @staticmethod
    def resolve_delivery_agencies(_, __):
        return DeliveryAgency.objects.all()


class Mutation(graphene.ObjectType):
    read_notifications = ReadNotifications.Field()
    create_or_update_banner = CreateOrUpdateBanner.Field()
    create_or_update_bank_account = CreateOrUpdateBankAccount.Field()
    delete_bank_account = DeleteInfoBankAccount.Field()
    create_or_update_additional_delivery_price = CreateOrUpdateAdditionalDeliveryPrice.Field()
    update_membership = UpdateMembership.Field()
    create_or_update_delivery_agency = CreateOrUpdateDeliveryAgency.Field()
    delete_info_delivery = DeleteDeliveryAgency.Field()
    update_extra_price_delivery = UpdateExtraPriceDelivery.Field()
    create_or_update_notice = CreateOrUpdateNoice.Field()
    delete_notice = DeleteNotice.Field()
    create_or_update_faq = CreateOrUpdateFaq.Field()
    delete_faq = DeleteFaq.Field()
    read_notification = ReadNotification.Field()
    create_or_update_address = CreateOrUpdateAddress.Field()
    delete_address = DeleteAddress.Field()


schema = graphene.Schema(query=Query)
