# -*- coding: utf-8 -*-
# Copyright 2017 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            if (
                    inv.fiscal_position and
                    inv.fiscal_position.with_fiscal_agent and
                    inv.intrastat
            ):
                vals = self.prepare_agent_invoice_vals()
                # set agent_invoce as 'Subject to Intrastat'
                vals.update({'intrastat': True})
                agent_invoice = self.create_write_agent_invoice(vals)
                # compute intrastat lines on agent_invoice
                agent_invoice.compute_intrastat_lines()
                agent_invoice.signal_workflow('invoice_open')
        return res
