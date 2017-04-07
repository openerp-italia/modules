# -*- coding: utf-8 -*-
# Copyright 2017 Alex Comba - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    def is_fiscal_agent_intrastat(self):
        if (
            self.fiscal_position and
            self.fiscal_position.with_fiscal_agent and
            self.fiscal_position.sudo().fiscal_agent_position_id and
            self.fiscal_position.sudo().fiscal_agent_position_id.
            intrastat
        ):
            return True
        else:
            return False

    @api.multi
    def create_write_agent_invoice(self, agent_invoice_vals):
        self.ensure_one()
        other_invoice = super(AccountInvoice, self).create_write_agent_invoice(
            agent_invoice_vals)
        if self.is_fiscal_agent_intrastat():
            # compute intrastat lines on agent_invoice
            other_invoice.compute_intrastat_lines()
        return other_invoice

    @api.multi
    def prepare_agent_invoice_vals(self):
        self.ensure_one()
        vals = super(AccountInvoice, self).prepare_agent_invoice_vals()
        if self.is_fiscal_agent_intrastat():
            # set agent_invoce as 'Subject to Intrastat'
            vals.update({'intrastat': True})
        return vals
