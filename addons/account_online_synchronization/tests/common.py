# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, fields
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class AccountOnlineSynchronizationCommon(AccountTestInvoicingCommon):

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)

        cls.gold_bank_journal = cls.env['account.journal'].create({
            'name': 'Gold Bank Journal',
            'type': 'bank',
            'code': 'GOLB',
            'currency_id': cls.currency_data['currency'].id,
        })
        cls.account_online_link = cls.env['account.online.link'].create({
            'name': 'Test Bank',
            'client_id': 'client_id_1',
            'refresh_token': 'refresh_token',
            'access_token': 'access_token',
        })
        cls.account_online_account = cls.env['account.online.account'].create({
            'name': 'MyBankAccount',
            'account_online_link_id': cls.account_online_link.id,
            'journal_ids': [Command.set(cls.gold_bank_journal.id)]
        })
        cls.BankStatementLine = cls.env['account.bank.statement.line']

    def setUp(self):
        super().setUp()
        self.transaction_id = 1
        self.account_online_account.balance = 0.0

    def _create_one_online_transaction(self, transaction_identifier=None, date=None, payment_ref=None, amount=10.0, partner_name=None):
        """ This method allows to create an online transaction granularly

            :param transaction_identifier: Online identifier of the transaction, by default transaction_id from the
                                           setUp. If used, transaction_id is not incremented.
            :param date: Date of the transaction, by default the date of today
            :param payment_ref: Label of the transaction
            :param amount: Amount of the transaction, by default equals 10.0
            :return: A dictionnary representing an online transaction (not formatted)
        """
        transaction_identifier = transaction_identifier or self.transaction_id
        if date:
            date = date if isinstance(date, str) else fields.Date.to_string(date)
        else:
            date = fields.Date.to_string(fields.Date.today())

        payment_ref = payment_ref or f'transaction_{transaction_identifier}'
        return {
            'online_transaction_identifier': transaction_identifier,
            'date': date,
            'payment_ref': payment_ref,
            'amount': amount,
            'partner_name': partner_name,
        }

    def _create_online_transactions(self, dates):
        """ This method returns a list of transactions with the
            given dates.
            All amounts equals 10.0

            :param dates: A list of dates, one transaction is created for each given date.
            :return: A formatted list of transactions
        """
        transactions = []
        for date in dates:
            transactions.append(self._create_one_online_transaction(date=date))
            self.transaction_id += 1
        return self.account_online_account._format_transactions(transactions)
