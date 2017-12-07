# -*- coding: utf-8 -*-
# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def onchange_partner_id_with_date(self, partner_id, date_order):
        res = self.onchange_partner_id(part=partner_id)
        if partner_id and date_order:
            dichiarazioni = self.env['dichiarazione.intento'].get_valid(
                partner_id, date_order)
            if dichiarazioni:
                res['value']['fiscal_position'] = \
                    dichiarazioni.fiscal_position_id.id
        return res
