import graphene


class BankPaymentInputType(graphene.InputObjectType):
    account_from = graphene.String()
    account_to = graphene.String()
    account_transaction_seq_no = graphene.String()
    account_balance_after_transaction = graphene.Int()
    account_result_code = graphene.String()
    account_in_print_content = graphene.String()
