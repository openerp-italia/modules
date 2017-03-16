# -*- coding: utf-8 -*-
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import api, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    def is_fiscal_agent_reverse_charge(self):
        if (
            self.fiscal_position and
            self.fiscal_position.with_fiscal_agent and
            self.fiscal_position.sudo().fiscal_agent_position_id and
            self.fiscal_position.sudo().fiscal_agent_position_id.
            rc_type_id
        ):
            return True
        else:
            return False

    @api.multi
    def prepare_agent_invoice_vals(self):
        self.ensure_one()
        vals = super(AccountInvoice, self).prepare_agent_invoice_vals()
        if self.is_fiscal_agent_intrastat():
            new_invoice_line_list = []
            invoice_line_list = vals['invoice_line']
            for line_tuple in invoice_line_list:
                invoice_line_vals = line_tuple[2]
                invoice_line_vals['rc'] = True
                new_invoice_line_list.append((0, 0, invoice_line_vals))
            vals['invoice_line'] = new_invoice_line_list
        return vals
