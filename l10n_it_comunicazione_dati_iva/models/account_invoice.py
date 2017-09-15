# -*- coding: utf-8 -*-


from openerp import api, fields, models, _


class account_invoice(models.Model):
    _inherit = "account.invoice"

    def _get_tax_comunicazione_dati_iva(self):
        for fattura in self:
            tax_lines = []
            for tax_line in fattura.tax_line:
                # aliquota
                aliquota = 0
                domain = [('tax_code_id', '=', tax_line.tax_code_id.id)]
                tax = self.env['account.tax'].search(
                    domain, order='id', limit=1)
                if tax:
                    aliquota = tax.amount * 100
                val = {
                    'ImponibileImporto': tax_line.base_amount,
                    'Imposta': tax_line.amount,
                    'Aliquota': aliquota,
                }
                tax_lines.append((0, 0, val))
        return tax_lines
