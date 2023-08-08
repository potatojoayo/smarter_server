import graphene


class CardPaymentInputType(graphene.InputObjectType):
    card_company = graphene.String()
    card_number = graphene.String()
    card_status = graphene.String()
    card_transaction_key = graphene.String()
    card_last_transaction_key = graphene.String()
    card_payment_key = graphene.String()
    card_balance_amount = graphene.Int()
    card_supplied_amount = graphene.Int()
    card_vat = graphene.Int()
    card_tax_free_amount = graphene.Int()
    card_currency = graphene.String()
    