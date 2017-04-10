# -*- coding: utf-8 -*-
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'
    # we need this to be able to call l10n_it_ddt.delivery_data
    note = fields.Text(
        'Additional Information', readonly=True, related="comment")
