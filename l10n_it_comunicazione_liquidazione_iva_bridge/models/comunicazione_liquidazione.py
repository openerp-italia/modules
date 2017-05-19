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

    def _get_tax_code(self, vat_account_ids, date_start, date_end):
        tax_code_ids = []
        if vat_account_ids:
            sql_filters = {
                'vat_account_ids': tuple(vat_account_ids)}
            sql = """
            SELECT tax_code_id
                from account_move_line ml
                left join account_tax_code txc ON 
                    (txc.vat_statement_account_id = ml.account_id)
                left join account_period per ON (per.id = ml.period_id)
            WHERE per.special = False AND date >= '{}' AND date <= '{}'
            """.format(date_start, date_end)
            sql += ' AND ml.account_id IN %(vat_account_ids)s '
            # Group
            sql += ' GROUP BY ml.tax_code_id '
            self.env.cr.execute(sql, sql_filters)
            items = self.env.cr.dictfetchall()
            for item in items:
                tax_code_ids.append(item['tax_code_id'])
        return tax_code_ids

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
                    vat_account_ids = []
                    debit_tax_code_ids = []
                    for debit in liq.debit_vat_account_line_ids:
                        if debit.account_id.id not in vat_account_ids:
                            vat_account_ids.append(debit.account_id.id)
                    if vat_account_ids:
                        debit_tax_code_ids = self._get_tax_code(
                            vat_account_ids, date_start, date_stop)
                        if debit_tax_code_ids:
                            tax_amounts = self.env['account.tax.code'].\
                                _get_tax_codes_amounts(
                                period.id, debit_tax_code_ids)
                            for tax in tax_amounts:
                                comunicazione.imponibile_operazioni_attive +=\
                                    tax_amounts[tax]['base']
                    # Operazioni passive
                    vat_account_ids = []
                    credit_tax_code_ids = []
                    for credit in liq.credit_vat_account_line_ids:
                        if credit.account_id.id not in vat_account_ids:
                            vat_account_ids.append(credit.account_id.id)
                    if vat_account_ids:
                        credit_tax_code_ids = self._get_tax_code(
                            vat_account_ids, date_start, date_stop)
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
