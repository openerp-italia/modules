# -*- coding: utf-8 -*-
# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    dichiarazione_intento_ids = fields.Many2many(
        'dichiarazione.intento', string='Dichiarazioni di Intento')

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
                            payment_term=False, partner_bank_id=False,
                            company_id=False):
        res = super(AccountInvoice, self).onchange_partner_id(
            type, partner_id, date_invoice, payment_term, partner_bank_id,
            company_id)
        if partner_id and date_invoice and type:
            dichiarazioni = self.env['dichiarazione.intento'].get_valid(
                type.split('_')[0],
                partner_id,
                date_invoice)
            if dichiarazioni:
                if not res:
                    res = {}
                res['value']['fiscal_position'] = \
                    dichiarazioni.fiscal_position_id.id
        return res

    @api.multi
    def onchange_payment_term_date_invoice_with_partner(
            self, payment_term_id, date_invoice, partner_id, type):
        res = self.onchange_payment_term_date_invoice(
            payment_term_id, date_invoice)
        if partner_id and date_invoice and type:
            type = 'out' if 'out' in type else 'in'
            dichiarazioni = self.env['dichiarazione.intento'].get_valid(
                type, partner_id, date_invoice)
            if dichiarazioni:
                if not res:
                    res = {}
                res['value']['fiscal_position'] = \
                    dichiarazioni.fiscal_position_id.id
        return res

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        dichiarazione_model = self.env['dichiarazione.intento']
        tax_model = self.env['account.tax']

        # ----- Assign account move lines to dichiarazione for invoices
        for invoice in self:
            dichiarazioni = dichiarazione_model.with_context(
                ignore_state=True if invoice.type.endswith('_refund')
                else False).get_valid(type=invoice.type.split('_')[0],
                                      partner_id=invoice.partner_id.id,
                                      date=invoice.date_invoice)
            # ----- If partner hasn't dichiarazioni, do nothing
            if not dichiarazioni:
                continue
            sign = 1 if invoice.type.startswith('out_') else -1
            # ----- Get only lines with taxes
            lines = invoice.move_id.line_id.filtered(lambda l: l.tax_code_id)
            if not lines:
                continue
            # ----- Group lines for tax
            grouped_lines = {}
            for line in lines:
                field_to_search = 'ref_base_code_id' \
                    if invoice.type.endswith('_refund') else 'base_code_id'
                tax = tax_model.search(
                    [(field_to_search, '=', line.tax_code_id.id), ], limit=1)
                if not tax:
                    continue
                # ----- Check if tax is in any dichiarazione:
                if tax.id not in [t.id
                                  for d in dichiarazioni
                                  for t in d.taxes_ids]:
                    continue
                if tax not in grouped_lines.keys():
                    grouped_lines.update({tax: []})
                grouped_lines[tax].append(line)
            # ----- Create a detail in dichiarazione for every tax group
            for tax, tax_lines in grouped_lines.iteritems():
                total_tax_amount = sign * sum([t.tax_amount for t in tax_lines])
                for dichiarazione in dichiarazioni:
                    if total_tax_amount <= dichiarazione.available_amount:
                        amount_value = total_tax_amount
                        total_tax_amount = 0.0
                    elif total_tax_amount > dichiarazione.available_amount:
                        amount_value = dichiarazione.available_amount
                        total_tax_amount -= dichiarazione.available_amount
                    else:
                        amount_value = 0.0
                    values = {
                        'taxes_ids': [(6, 0, [tax.id, ])],
                        'move_line_ids': [(6, 0,
                                           [l.id for l in tax_lines])],
                        'amount': amount_value,
                        'invoice_id': invoice.id,
                        'base_amount': invoice.amount_untaxed,
                        'currency_id': invoice.currency_id.id,
                        }
                    dichiarazione.line_ids = [(0, 0, values)]
                    # ----- Link dichiarazione to invoice
                    invoice.dichiarazione_intento_ids = [
                        (4, dichiarazione.id)]
                if total_tax_amount > 0.0:
                    raise UserError(
                        'Available plafond insufficent.\n'
                        'Excess value: %s' % total_tax_amount)
        return res

    @api.multi
    def action_cancel(self):
        line_model = self.env['dichiarazione.intento.line']
        for invoice in self:
            # ----- Force unlink of dichiarazione details to compute used
            #       amount field
            lines = line_model.search([('invoice_id', '=', invoice.id)])
            if lines:
                for line in lines:
                    invoice.dichiarazione_intento_ids = [
                        (3, line.dichiarazione_id.id)]
                lines.unlink()
        return super(AccountInvoice, self).action_cancel()
