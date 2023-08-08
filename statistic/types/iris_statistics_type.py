import graphene


class IrisStatisticsType(graphene.ObjectType):
    total_cash_payment = graphene.Int()
    total_card_payment = graphene.Int()
    total_bank_account_payment = graphene.Int()
    total_smarter_money_payment = graphene.Int()
    total_payment = graphene.Int()
    refund_amount = graphene.Int()
    total_sales_payment = graphene.Int()
    total_profit_amount = graphene.Int()
    total_product_price = graphene.Int()
    total_work_price = graphene.Int()
    total_work_labor_price = graphene.Int()
    total_order_price = graphene.Int()
    total_delivery_price = graphene.Int()
    total_price = graphene.Int()
    date_from = graphene.String()
    date_to = graphene.String()
