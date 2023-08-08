from datetime import datetime
import locale
import graphene
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from graphene import relay

from cs.types.smarter_money_histories_type import SmarterMoneyHistoriesType
from .fields import MyHistoryField, ChargeOrderField
from smarter_money.models import Wallet, ChargeOrder, SmarterMoneyHistory
from smarter_money.mutations.charge_smarter_money import ChargeSmarterMoney
from smarter_money.types.smarter_money_history_node import SmarterMoneyHistoryNode
from smarter_money.types.wallet_type import WalletType
from .mutations.bulk_charge_smarter_money import BulkChargeSmarterMoney
from .mutations.create_charge_order import CreateChargeOrder
from .types.charge_order_node import ChargeOrderNode

from django.db.models import Func

from .types.smarter_money_histories import SmarterMoneyHistories
from .types.wallets_type import WalletsType

ko_kr = Func(
    "wallet__user__gym__name",
    function="ko_KR.utf8",
    template='(%(expressions)s) COLLATE "%(function)s"'
)

class Query(graphene.ObjectType):
    my_wallet = graphene.Field(WalletType)

    smarter_money_history = relay.node.Field(SmarterMoneyHistoryNode)
    my_smarter_money_histories = MyHistoryField(SmarterMoneyHistoryNode)
    charge_orders = ChargeOrderField(ChargeOrderNode, keyword=graphene.String())
    today_charge_order_count_by_state = graphene.Int(state=graphene.String())
    gyms_smarter_money_histories = graphene.Field(SmarterMoneyHistoriesType, keyword=graphene.String(), year=graphene.Int(), month=graphene.Int(), page=graphene.Int())
    wallets = graphene.Field(WalletsType, page=graphene.Int(), keyword=graphene.String(), sort_type=graphene.String())

    @staticmethod
    def resolve_wallets(_, __, page, sort_type=None, **kwargs):
        keyword = kwargs.get('keyword')
        wallets = Wallet.objects.filter(user__groups__name="체육관")
        q = Q()
        if keyword:
            q.add(Q(user__identification__icontains=keyword) | Q(user__gym__name__icontains=keyword) | Q(user__phone=keyword), q.AND)
            wallets = wallets.filter(q)
        if sort_type:
            if sort_type == "보유잔액순":
                wallets = wallets.order_by('-balance')

        total_count = wallets.count()
        return WalletsType(wallets=wallets[10*(page-1): 10*page],
                           total_count=total_count)

    @staticmethod
    def resolve_gyms_smarter_money_histories(_, __,year,  month, page,  **kwargs):
        keyword = kwargs.get('keyword')
        date = datetime(year=year, month=month, day=1)
        smarter_money_histories = SmarterMoneyHistory.objects.filter(date_created__gte=date,
                                                                     date_created__lt=date+relativedelta(months=1))
        if keyword:
            q = Q()
            if keyword.isdigit():
                q.add(Q(amount=keyword) | Q(wallet__balance=keyword), q.OR)
            q.add(Q(wallet__user__identification__icontains=keyword) | Q(wallet__user__phone__icontains=keyword) | Q(wallet__user__gym__name__icontains=keyword) , q.OR)
            smarter_money_histories = smarter_money_histories.filter(q)

        smarter_money_histories = smarter_money_histories.order_by('-date_created')
        total_count = smarter_money_histories.count()
        return SmarterMoneyHistoriesType(smarter_money_histories=smarter_money_histories[10*(page-1): 10*page],
                                         total_count=total_count)

    @staticmethod
    def resolve_my_wallet(_, info):
        return Wallet.objects.get(user=info.context.user)

    @staticmethod
    def resolve_today_charge_order_count_by_state(_, __, state):
        if state == '전체':
            return ChargeOrder.objects.all().distinct().count()
        return ChargeOrder.objects.filter(
            state=state,
        ).distinct().count()


class Mutation(graphene.ObjectType):

    charge_smarter_money = ChargeSmarterMoney.Field()
    bulk_charge_smarter_money = BulkChargeSmarterMoney.Field()
    create_charge_order = CreateChargeOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
