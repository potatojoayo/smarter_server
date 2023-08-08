import graphene

from smarter_money.types.wallet_type import WalletType


class WalletsType(graphene.ObjectType):
    class Meta:
        description = 'sort_type: ["보유잔액순", "가나다순"]'
    wallets = graphene.List(WalletType)
    total_count = graphene.Int()