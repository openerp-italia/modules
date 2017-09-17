# -*- coding: utf-8 -*-


from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


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
                    'Natura_id': tax.kind_id.id if tax.kind_id else False,
                    'EsigibilitaIVA': tax.payability
                    if tax.payability else False,
                }
                val = self._check_tax_comunicazione_dati_iva(tax, val)
                tax_lines.append((0, 0, val))
        return tax_lines

    def _check_tax_comunicazione_dati_iva(self, tax, val=None):
        if not val:
            val = {}
        if val['Aliquota'] == 0 and not val['Natura_id']:
            raise ValidationError(
                _("Specificare la natura dell'esenzione per l'imposta: {}"
                  ).format(tax.name))
        if not val['EsigibilitaIVA']:
            raise ValidationError(
                _("Specificare l'esigibilità IVA per l'imposta: {}"
                  ).format(tax.name))

        return val
