from django.db import models

from order.models.order_master import OrderMaster


class Payment(models.Model):

    order_master = models.ForeignKey(OrderMaster, on_delete=models.CASCADE, related_name='payments')
    pay_method = models.CharField(max_length=20)
    amount = models.IntegerField()

    # 계좌이체 시
    account_from = models.CharField(max_length=50, null=True, blank=True)
    account_to = models.CharField(max_length=50, null=True, blank=True)
    account_transaction_seq_no = models.CharField(max_length=10, null=True, blank=True)
    account_balance_after_transaction = models.IntegerField(null=True, blank=True)
    account_result_code = models.CharField(max_length=10, null=True, blank=True)
    account_in_print_content = models.CharField(max_length=50, null=True, blank=True)

    # 카드 결제 시 (토스페이먼츠)
    card_company = models.CharField(max_length=20)
    card_number = models.CharField(max_length=50)
    card_status = models.CharField(max_length=10, null=True, blank=True)
    card_transaction_key = models.CharField(max_length=50, null=True, blank=True)
    card_last_transaction_key = models.CharField(max_length=50, null=True, blank=True)
    card_payment_key = models.CharField(max_length=100, null=True, blank=True)
    card_balance_amount = models.IntegerField(null=True, blank=True)
    card_supplied_amount = models.IntegerField(null=True, blank=True)
    card_vat = models.IntegerField(null=True, blank=True)
    card_tax_free_amount = models.IntegerField(null=True, blank=True)
    card_currency = models.CharField(max_length=20, null=True, blank=True)

    # DATE
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_created)


