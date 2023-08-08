from common.models import BankAccount


def get_bank_infos():
    bank_accounts = BankAccount.objects.filter(is_active=True)

    bank_infos = ''

    for index, bank_account in enumerate(bank_accounts):
        bank_infos += '{} {} [예금주: {}] '.format(bank_account.refund_bank_name, bank_account.account_no, bank_account.owner_name)
        if index < bank_accounts.count()-1:
            bank_infos += ' 또는, '

    return bank_infos
