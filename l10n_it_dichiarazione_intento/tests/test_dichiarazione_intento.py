# -*- coding: utf-8 -*-
# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from openerp import fields
from openerp.exceptions import Warning as UserError, ValidationError
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class TestDichiarazioneIntento(TransactionCase):

    def _create_dichiarazione(self, partner):
        return self.env['dichiarazione.intento'].sudo().create({
            'partner_id': partner.id,
            'partner_document_number': 'PartnerTest%s' % partner.id,
            'partner_document_date': self.today_date,
            'date': self.today_date,
            'date_start': self.today_date,
            'date_end': self.today_date,
            'taxes_ids': [(6, 0, [self.tax1.id])],
            'limit_amount': 1000.00,
            'fiscal_position_id': self.fiscal_position.id,
            })

    def _create_invoice(self, partner, tax=False, date=False):
        invoice_date = date if date else self.today_date
        payment_term = self.env.ref('account.account_payment_term_advance')
        account = self.env.ref('l10n_it.1_1501')
        invoice_line_data = [(0, 0, {
            'product_id': self.env.ref('product.product_product_5').id,
            'quantity': 10.00,
            'account_id': self.env.ref('l10n_it.1_3101').id,
            'name': 'test line',
            'price_unit': 90.00,
            'invoice_line_tax_ids': [(6, 0, [tax.id])] if tax else False,
            })]
        return self.env['account.invoice'].sudo().create({
            'partner_id': partner.id,
            'date_invoice': invoice_date,
            'type': 'out_invoice',
            'name': 'Test Invoice for Dichiarazione',
            'reference_type': 'none',
            'payment_term_id': payment_term.id,
            'account_id': account.id,
            'invoice_line_ids': invoice_line_data,
            })

    def _create_refund(self, partner, tax=False, date=False, invoice=False):
        invoice_date = date if date else self.today_date
        payment_term = self.env.ref('account.account_payment_term_advance')
        account = self.env.ref('l10n_it.1_1501')
        invoice_line_data = [(0, 0, {
            'quantity': 1.00,
            'account_id': self.env.ref('l10n_it.1_3101').id,
            'name': 'test refund line',
            'price_unit': 100.00,
            'invoice_line_tax_ids': [(6, 0, [tax.id])] if tax else False,
            })]
        return self.env['account.invoice'].sudo().create({
            'partner_id': partner.id,
            'date_invoice': invoice_date,
            'type': 'out_refund',
            'name': 'Test Refund for Dichiarazione',
            'reference_type': 'none',
            'payment_term_id': payment_term.id,
            'account_id': account.id,
            'invoice_line_ids': invoice_line_data,
            'refund_invoice_id': invoice.id,
            })

    def setUp(self):
        super(TestDichiarazioneIntento, self).setUp()
        self.today_date = fields.Date.today()
        self.partner1 = self.env.ref('base.res_partner_2')
        self.partner2 = self.env.ref('base.res_partner_12')
        self.tax1 = self.env.ref('l10n_it.1_00v INC')
        self.fiscal_position = self.env[
            'account.fiscal.position'].sudo().create({
                'name': 'Dichiarazione Test',
                'valid_for_dichiarazione_intento': True,
                'tax_ids': [(0, 0, {
                    'tax_src_id': self.env.ref('l10n_it.1_10v').id,
                    'tax_dest_id': self.tax1.id,
                    })]
                })
        self.fiscal_position_with_wrong_taxes = self.env[
            'account.fiscal.position'].sudo().create({
                'name': 'Dichiarazione Test Wrong',
                'valid_for_dichiarazione_intento': True,
                'tax_ids': [(0, 0, {
                    'tax_src_id': self.env.ref('l10n_it.1_10v').id,
                    'tax_dest_id': self.env.ref('l10n_it.1_22v').id,
                    })]
                })
        self.dichiarazione1 = self._create_dichiarazione(self.partner1)
        self.dichiarazione2 = self._create_dichiarazione(self.partner2)
        self.dichiarazione3 = self._create_dichiarazione(self.partner2)
        self.invoice1 = self._create_invoice(self.partner1)
        self.invoice2 = self._create_invoice(self.partner1, tax=self.tax1)
        self.invoice3 = self._create_invoice(self.partner1, tax=self.tax1)
        self.invoice_without_valid_taxes = self._create_invoice(
            self.partner1, tax=self.env.ref('l10n_it.1_2v'))
        future_date = datetime.today() + timedelta(days=10)
        future_date = future_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        self.invoice_future = self._create_invoice(self.partner1,
                                                   date=future_date,
                                                   tax=self.tax1)
        self.refund1 = self._create_refund(self.partner1, tax=self.tax1,
                                           invoice=self.invoice2)

    def test_dichiarazione_data(self):
        self.assertTrue(self.dichiarazione1.number)

    def test_costraints(self):
        with self.assertRaises(ValidationError):
            self.dichiarazione1.fiscal_position_id = \
                self.fiscal_position_with_wrong_taxes.id

    def test_get_valid(self):
        dichiarazione_model = self.env['dichiarazione.intento'].sudo()
        self.assertFalse(dichiarazione_model.get_valid())
        records = dichiarazione_model.get_valid(partner_id=self.partner1.id,
                                                date=self.today_date)
        self.assertEquals(len(records), 1)
        records = dichiarazione_model.get_valid(partner_id=self.partner2.id,
                                      date=self.today_date)
        self.assertEquals(len(records), 2)

    def test_dichiarazione_state_change(self):
        self.assertEqual(self.dichiarazione1.state, 'valid')
        # ----- Close dichiarazione by moving end date before today
        previuos_date = datetime.today() - timedelta(days=10)
        self.dichiarazione1.date_start = previuos_date.strftime(
            DEFAULT_SERVER_DATE_FORMAT)
        self.dichiarazione1.date_end = previuos_date.strftime(
            DEFAULT_SERVER_DATE_FORMAT)
        self.assertEqual(self.dichiarazione1.state, 'close')

    def test_invoice_validation_with_no_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice1.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)
        self.invoice_future.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)
        self.invoice_without_valid_taxes.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_invoice_reopen_with_no_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice1.action_invoice_open()
        self.invoice1.action_invoice_cancel()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_invoice_validation_under_dichiarazione_limit(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice2.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertNotEqual(previous_used_amount, post_used_amount)

    def test_invoice_validation_over_dichiarazione_limit(self):
        self.invoice2.action_invoice_open()
        with self.assertRaises(UserError):
            self.invoice3.action_invoice_open()

    def test_invoice_reopen_with_effect_on_dichiarazione(self):
        previous_used_amount = self.dichiarazione1.used_amount
        self.invoice2.action_invoice_open()
        self.invoice2.action_invoice_cancel()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertEqual(previous_used_amount, post_used_amount)

    def test_refund(self):
        self.invoice2.action_invoice_open()
        previous_used_amount = self.dichiarazione1.used_amount
        self.refund1.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        self.assertNotEqual(previous_used_amount, post_used_amount)

    def test_refund_with_amount_bigger_than_residual(self):
        self.invoice2.action_invoice_open()
        previous_used_amount = self.dichiarazione1.used_amount
        self.refund1.invoice_line_ids[0].quantity = 10
        self.refund1.action_invoice_open()
        post_used_amount = self.dichiarazione1.used_amount
        print '============', self.dichiarazione1.used_amount
        self.assertNotEqual(previous_used_amount, post_used_amount)
