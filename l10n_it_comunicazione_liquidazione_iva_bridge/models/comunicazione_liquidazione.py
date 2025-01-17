# -*- coding: utf-8 -*-


from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class ComunicazioneLiquidazioneVp(models.Model):
    _inherit = 'comunicazione.liquidazione.vp'

    liquidazioni_ids = fields.Many2many(
        'account.vat.period.end.statement',
        'comunicazione_iva_liquidazioni_rel',
        'comunicazione_id',
        'liquidazione_id',
        string='Liquidazioni')

    def _reset_values(self):
        for quadro in self:
            quadro.imponibile_operazioni_attive = 0
            quadro.imponibile_operazioni_passive = 0
            quadro.iva_esigibile = 0
            quadro.iva_detratta = 0
            quadro.debito_periodo_precedente = 0
            quadro.credito_periodo_precedente = 0
            quadro.credito_anno_precedente = 0
            quadro.versamento_auto_UE = 0
            quadro.crediti_imposta = 0
            quadro.interessi_dovuti = 0
            quadro.accounto_dovuto = 0

    @api.multi
    @api.onchange('liquidazioni_ids')
    def compute_from_liquidazioni(self):

        for quadro in self:
            # Reset valori
            quadro._reset_values()

            interests_account_id = quadro.comunicazione_id.company_id.\
                of_account_end_vat_statement_interest_account_id.id or False

            for liq in quadro.liquidazioni_ids:

                for period in liq.period_ids:
                    date_start = period.date_start
                    date_stop = period.date_stop
                    # Operazioni attive
                    debit_tax_code_ids = []
                    for debit in liq.debit_vat_account_line_ids:
                        debit_tax_code_ids.append(debit.tax_code_id.id)
                    if debit_tax_code_ids:
                        tax_amounts = self.env['account.tax.code'].\
                            _get_tax_codes_amounts(
                                period.id, debit_tax_code_ids)
                        for tax in tax_amounts:
                            quadro.imponibile_operazioni_attive +=\
                                tax_amounts[tax]['base']

                    # Operazioni passive
                    credit_tax_code_ids = []
                    for credit in liq.credit_vat_account_line_ids:
                        credit_tax_code_ids.append(credit.tax_code_id.id)
                    if credit_tax_code_ids:
                        tax_amounts = self.env['account.tax.code'].\
                            _get_tax_codes_amounts(
                                period.id, credit_tax_code_ids)
                        for tax in tax_amounts:
                            quadro.imponibile_operazioni_passive +=\
                                -1 * tax_amounts[tax]['base']
                # Iva esigibile
                for vat_amount in liq.debit_vat_account_line_ids:
                    quadro.iva_esigibile += vat_amount.amount
                # Iva detratta
                for vat_amount in liq.credit_vat_account_line_ids:
                    quadro.iva_detratta += vat_amount.amount
                # credito/debito periodo precedente
                quadro.debito_periodo_precedente =\
                    liq.previous_debit_vat_amount
                quadro.credito_periodo_precedente =\
                    liq.previous_credit_vat_amount
                # Credito anno precedente (NON GESTITO)
                # Versamenti auto UE (NON GESTITO)
                # Crediti d’imposta (NON GESTITO)
                # Da altri crediti e debiti calcolo:
                # 1 - Interessi dovuti per liquidazioni trimestrali
                # 2 - Decremento iva esigibile con righe positive
                # 3 - Decremento iva detratta con righe negative
                for line in liq.generic_vat_account_line_ids:
                    if interests_account_id and \
                            (line.account_id.id == interests_account_id):
                        quadro.interessi_dovuti += (-1 * line.amount)
                    elif line.amount > 0:
                        quadro.iva_esigibile -= line.amount
                    else:
                        quadro.iva_detratta += line.amount
