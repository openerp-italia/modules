# -*- coding: utf-8 -*-


from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class ComunicazioneLiquidazione(models.Model):
    _inherit = 'comunicazione.liquidazione'

    liquidazioni_ids = fields.Many2many(
        'account.vat.period.end.statement',
        'comunicazione_iva_liquidazioni_rel',
        'comunicazione_id',
        'liquidazione_id',
        string='Liquidazioni')

    def _reset_values(self):
        for comunicazione in self:
            comunicazione.imponibile_operazioni_attive = 0
            comunicazione.imponibile_operazioni_passive = 0
            comunicazione.iva_esigibile = 0
            comunicazione.iva_detratta = 0
            comunicazione.debito_periodo_precedente = 0
            comunicazione.credito_periodo_precedente = 0
            comunicazione.credito_anno_precedente = 0
            comunicazione.versamento_auto_UE = 0
            comunicazione.crediti_imposta = 0
            comunicazione.interessi_dovuti = 0
            comunicazione.accounto_dovuto = 0

    @api.multi
    @api.onchange('liquidazioni_ids')
    def compute_from_liquidazioni(self):

        for comunicazione in self:
            # Reset valori
            comunicazione._reset_values()

            interests_account_id = comunicazione.company_id.\
                of_account_end_vat_statement_interest_account_id.id or False

            for liq in comunicazione.liquidazioni_ids:
                previous_debit = {
                    'date': False,
                    'amount': 0
                }
                previous_credit = {
                    'date': False,
                    'amount': 0
                }
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
                            comunicazione.imponibile_operazioni_attive +=\
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
                            comunicazione.imponibile_operazioni_passive +=\
                                -1 * tax_amounts[tax]['base']

                    # Debito periodo precedente (solo periodo + recente)
                    if not previous_debit['date'] \
                            or period.date_stop > previous_debit['date']:
                        previous_debit['date'] = period.date_stop
                        previous_debit['amount'] =\
                            liq.previous_debit_vat_amount
                    # Credito periodo precedente (solo periodo + recente)
                    if not previous_credit['date'] \
                            or period.date_stop > previous_credit['date']:
                        previous_credit['date'] = period.date_stop
                        previous_credit['amount'] =\
                            liq.previous_credit_vat_amount
                # Iva esigibile
                for vat_amount in liq.debit_vat_account_line_ids:
                    comunicazione.iva_esigibile += vat_amount.amount
                # Iva detratta
                for vat_amount in liq.credit_vat_account_line_ids:
                    comunicazione.iva_detratta += vat_amount.amount
                # credito/debito periodo precedente
                comunicazione.debito_periodo_precedente =\
                    previous_debit['amount']
                comunicazione.credito_periodo_precedente =\
                    previous_credit['amount']
                # Credito anno precedente (NON GESTITO)
                # Versamenti auto UE (NON GESTITO)
                # Crediti d’imposta (NON GESTITO)

                # Interessi dovuti per liquidazioni trimestrali
                interessi_dovuti = 0
                if interests_account_id:
                    for line in liq.generic_vat_account_line_ids:
                        if line.account_id.id == interests_account_id:
                            interessi_dovuti += line.amount
                comunicazione.interessi_dovuti += interessi_dovuti

                print "xxxx"
