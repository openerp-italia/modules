# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError, ValidationError
from xml.etree import ElementTree as etree


class ComunicazioneLiquidazione(models.Model):
    _name = 'comunicazione.liquidazione'
    _description = 'Comunicazione Liquidazione IVA'

    @api.model
    def _default_company(self):
        company_id = self._context.get(
            'company_id', self.env.user.company_id.id)
        return company_id

    @api.constrains('month')
    def _check_month(self):
        if self.period_type == 'month':
            if self.month not in range(1, 12):
                raise ValidationError(
                    _("Month valid: from 1 to 12"))

    @api.constrains('quoter')
    def _check_month(self):
        if self.period_type == 'quoter':
            if self.quoter not in range(1, 4):
                raise ValidationError(
                    _("Quoter valid: from 1 to 4"))

    @api.multi
    @api.depends('iva_esigibile', 'iva_detratta')
    def _compute_VP6_iva_dovuta_credito(self):
        for dich in self:
            dich.iva_dovuta_debito = 0
            dich.iva_dovuta_credito = 0
            if dich.iva_esigibile >= dich.iva_detratta:
                dich.iva_dovuta_debito = dich.iva_esigibile - dich.iva_detratta
            else:
                dich.iva_dovuta_credito = dich.iva_detratta - \
                    dich.iva_esigibile

    @api.multi
    @api.depends('iva_dovuta_debito', 'iva_dovuta_credito',
                 'debito_periodo_precedente', 'credito_periodo_precedente',
                 'credito_anno_precedente', 'versamento_auto_UE',
                 'crediti_imposta', 'interessi_dovuti', 'accounto_dovuto')
    def _compute_VP14_iva_da_versare_credito(self):
        """
        Tot Iva a debito = (VP6, col.1 + VP7 + VP12) 
        Tot Iva a credito = (VP6, col.2 + VP8 + VP9 + VP10 + VP11 + VP13)
        """
        for dich in self:
            dich.iva_da_versare = 0
            dich.iva_a_credito = 0
            debito = dich.iva_dovuta_debito + dich.debito_periodo_precedente\
                + dich.interessi_dovuti
            credito = dich.iva_dovuta_credito \
                + dich.credito_periodo_precedente\
                + dich.credito_anno_precedente \
                + dich.versamento_auto_UE + dich.crediti_imposta \
                + dich.accounto_dovuto
            if debito >= credito:
                dich.iva_da_versare = debito - credito
            else:
                dich.iva_a_credito = credito - debito

    def _compute_name(self):
        for dich in self:
            self.name = '{} {}'.format(str(dich.year), dich.period_type)
            if dich.period_type == 'month':
                self.name += ' {}'.format(str(dich.month))
            else:
                self.name += ' {}'.format(str(dich.quarter))

    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=_default_company)
    name = fields.Char(string='Name', compute="_compute_name")
    year = fields.Integer(string='Year', required=True, size=4)
    last_month = fields.Integer(string='Last month')
    liquidazione_del_gruppo = fields.Boolean(string='Liquidazione del gruppo')
    taxpayer_vat = fields.Char(string='Vat')
    controller_vat = fields.Char(string='Controller Vat')
    taxpayer_fiscalcode = fields.Char(string='Fiscalcode')
    declarant_different = fields.Boolean(
        string='Declarant different from taxpayer')
    declarant_fiscalcode = fields.Char(string='Fiscalcode')
    declarant_fiscalcode_company = fields.Char(string='Fiscalcode company')
    codice_carica_id = fields.Many2one('codce.carica', string='Codice carica')
    declarant_sign = fields.Boolean(string='Declarant sign')

    delegate_fiscalcode = fields.Char(string='Fiscalcode')
    delegate_commitment = fields.Selection(
        [('1', 'Comunicazione è stata predisposta dal contribuente '),
         ('2', 'Comunicazione è stata predisposta da chi effettua l’invio')],
        string='Commitment')
    delegate_sign = fields.Boolean(string='Delegate sign')
    date_commitment = fields.Date(string='Date commitment')
    date_start = fields.Date(string='Date start')
    date_stop = fields.Date(string='Date stop')

    period_type = fields.Selection(
        [('month', 'Monthly'),
         ('quarter', 'Quarterly')],
        string='Period type', default='quarter')
    month = fields.Integer(string='Month')
    quarter = fields.Integer(string='Quoter')
    subcontracting = fields.Boolean(string='Subcontracting')
    exceptional_events = fields.Selection(
        [('1', 'Code 1'), ('9', 'Code 9')], string='Exceptional events')

    imponibile_operazioni_attive = fields.Float(
        string='Totale operazioni attive (al netto dell’IVA)')
    imponibile_operazioni_passive = fields.Float(
        string='Totale operazioni passive (al netto dell’IVA)')
    iva_esigibile = fields.Float(string='IVA esigibile')
    iva_detratta = fields.Float(string='IVA detratta')
    iva_dovuta_debito = fields.Float(
        string='IVA dovuta debito',
        compute="_compute_VP6_iva_dovuta_credito", store=True)
    iva_dovuta_credito = fields.Float(
        string='IVA dovuta credito',
        compute="_compute_VP6_iva_dovuta_credito", store=True)
    debito_periodo_precedente = fields.Float(
        string='Debito periodo precedente')
    credito_periodo_precedente = fields.Float(
        string='Credito periodo precedente')
    credito_anno_precedente = fields.Float(string='Credito anno precedente')
    versamento_auto_UE = fields.Float(string='Versamenti auto UE')
    crediti_imposta = fields.Float(string='Crediti d’imposta')
    interessi_dovuti = fields.Float(
        string='Interessi dovuti per liquidazioni trimestrali')
    accounto_dovuto = fields.Float(string='Acconto dovuto')
    iva_da_versare = fields.Float(
        string='IVA da versare',
        compute="_compute_VP14_iva_da_versare_credito", store=True)
    iva_a_credito = fields.Float(
        string='IVA a credito',
        compute="_compute_VP14_iva_da_versare_credito", store=True)

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            self.taxpayer_vat = self.company_id.partner_id.vat
            self.taxpayer_fiscalcode = \
                self.company_id.partner_id.fiscalcode

    def get_export_xml(self):
        self._export_xml_validate()
        x1_Fornitura = etree.Element('Fornitura')

        x1_1_Intestazione = self._export_xml_get_intestazione_1_1(x1_Fornitura)

        x1_2_Comunicazione = etree.Element('Comunicazione')
        x1_2_1_Frontespizio = self._export_xml_get_frontespizio()
        x1_2_2_DatiContabili = self._export_xml_get_dati_contabili()
        x1_2_Comunicazione.append(x1_2_1_Frontespizio)
        x1_2_Comunicazione.append(x1_2_2_DatiContabili)
        # Composizione struttura xml con le varie sezioni generate
        x1_Fornitura.append(x1_1_Intestazione)
        x1_Fornitura.append(x1_2_Comunicazione)
        return etree.tostring(x1_Fornitura, encoding='utf8', method='xml')

    def _export_xml_validate(self):
        return True

    def _export_xml_get_intestazione_1_1(self, x1_Fornitura):
        x1_1_Intestazione = etree.Element('Intestazione')
        # Codice Fornitura
        x1_1_1_CodiceFornitura = etree.SubElement(
            x1_1_Intestazione, 'CodiceFornitura')
        x1_1_1_CodiceFornitura.text = unicode('IVP17')
        # Codice Fiscale Dichiarante
        if self.declarant_fiscalcode:
            x1_1_2_CodiceFiscaleDichiarante = etree.SubElement(
                x1_1_Intestazione, 'CodiceFiscaleDichiarante')
            x1_1_2_CodiceFiscaleDichiarante.text = unicode(
                self.declarant_fiscalcode)
        # Codice Carica
        if self.codice_carica_id:
            x1_1_3_CodiceCarica = etree.SubElement(
                x1_1_Intestazione, 'CodiceCarica')
            x1_1_3_CodiceCarica.text = unicode(self.codice_carica_id.code)
        return x1_1_Intestazione

    def _export_xml_get_frontespizio(self):
        x1_2_1_Frontespizio = etree.Element('Frontespizio')
        # Codice Fiscale
        x1_2_1_1_CodiceFiscale = etree.SubElement(
            x1_2_1_Frontespizio, 'CodiceFiscale')
        x1_2_1_1_CodiceFiscale.text = unicode(self.taxpayer_fiscalcode)
        # Anno Imposta
        x1_2_1_2_AnnoImposta = etree.SubElement(
            x1_2_1_Frontespizio, 'AnnoImposta')
        x1_2_1_2_AnnoImposta.text = str(self.year)
        # Partita IVA
        x1_2_1_3_PartitaIVA = etree.SubElement(
            x1_2_1_Frontespizio, 'PartitaIVA')
        x1_2_1_3_PartitaIVA.text = self.taxpayer_vat
        # PIVA Controllante
        if self.controller_vat:
            x1_2_1_4_PIVAControllante = etree.SubElement(
                x1_2_1_Frontespizio, 'PIVAControllante')
            x1_2_1_4_PIVAControllante.text = self.controller_vat
        # Ultimo Mese
        if self.last_month:
            x1_2_1_5_UltimoMese = etree.SubElement(
                x1_2_1_Frontespizio, 'UltimoMese')
            x1_2_1_5_UltimoMese.text = self.last_month
        # Liquidazione Gruppo
        x1_2_1_6_LiquidazioneGruppo = etree.SubElement(
            x1_2_1_Frontespizio, 'LiquidazioneGruppo')
        x1_2_1_6_LiquidazioneGruppo.text = \
            '1' if self.liquidazione_del_gruppo else '0'
        # CF Dichiarante
        if self.declarant_fiscalcode:
            x1_2_1_7_CFDichiarante = etree.SubElement(
                x1_2_1_Frontespizio, 'CFDichiarante')
            x1_2_1_7_CFDichiarante.text = self.declarant_fiscalcode
        # CodiceCaricaDichiarante
        if self.codice_carica_id:
            x1_2_1_8_CodiceCaricaDichiarante = etree.SubElement(
                x1_2_1_Frontespizio, 'CodiceCaricaDichiarante')
            x1_2_1_8_CodiceCaricaDichiarante.text = self.codice_carica_id.code
        # CodiceFiscaleSocieta
        if self.declarant_fiscalcode_company:
            x1_2_1_9_CodiceFiscaleSocieta = etree.SubElement(
                x1_2_1_Frontespizio, 'CodiceFiscaleSocieta')
            x1_2_1_9_CodiceFiscaleSocieta.text = self.declarant_fiscalcode_company.code
        # FirmaDichiarazione
        x1_2_1_10_FirmaDichiarazione = etree.SubElement(
            x1_2_1_Frontespizio, 'FirmaDichiarazione')
        x1_2_1_10_FirmaDichiarazione.text = '1' if self.declarant_sign else '0'
        # CFIntermediario
        if self.delegate_fiscalcode:
            x1_2_1_11_CFIntermediario = etree.SubElement(
                x1_2_1_Frontespizio, 'CFIntermediario')
            x1_2_1_11_CFIntermediario.text = self.delegate_fiscalcode
        # ImpegnoPresentazione
        if self.delegate_commitment:
            x1_2_1_12_ImpegnoPresentazione = etree.SubElement(
                x1_2_1_Frontespizio, 'ImpegnoPresentazione')
            x1_2_1_12_ImpegnoPresentazione.text = self.delegate_commitment
        # DataImpegno
        if self.date_commitment:
            x1_2_1_13_DataImpegno = etree.SubElement(
                x1_2_1_Frontespizio, 'DataImpegno')
            x1_2_1_13_DataImpegno.text = datetime.strptime(
                self.date_commitment, "%Y-%m-%d").strftime('%d%m%Y')
        # FirmaIntermediario
        x1_2_1_14_FirmaIntermediario = etree.SubElement(
            x1_2_1_Frontespizio, 'FirmaIntermediario')
        x1_2_1_14_FirmaIntermediario.text = '1' if self.delegate_sign else '0'

        return x1_2_1_Frontespizio

    def _export_xml_get_dati_contabili(self):
        x1_2_2_DatiContabili = etree.Element('DatiContabili')
        # Modulo
        x1_2_2_1_Modulo = etree.SubElement(
            x1_2_2_DatiContabili, 'Modulo')
        if self.period_type == 'month':
            # Mese
            x1_2_2_1_1_Mese = etree.SubElement(
                x1_2_2_1_Modulo, 'Mese')
            x1_2_2_1_1_Mese.text = str(self.month)
        else:
            # Trimestre
            x1_2_2_1_2_Trimestre = etree.SubElement(
                x1_2_2_1_Modulo, 'Trimestre')
            x1_2_2_1_2_Trimestre.text = str(self.quarter)
        # Subfornitura
        x1_2_2_1_3_Subfornitura = etree.SubElement(
            x1_2_2_DatiContabili, 'Subfornitura')
        x1_2_2_1_3_Subfornitura.text = '1' if self.subcontracting else '0'
        # EventiEccezionali
        if self.exceptional_events:
            x1_2_2_1_3_EventiEccezionali = etree.SubElement(
                x1_2_2_DatiContabili, 'EventiEccezionali')
            x1_2_2_1_3_EventiEccezionali.text = self.exceptional_events
        # 1.2.2.1.5  TotaleOperazioniAttive
        TotaleOperazioniAttive = etree.SubElement(
            x1_2_2_DatiContabili, 'TotaleOperazioniAttive')
        TotaleOperazioniAttive.text = "{:.2f}"\
            .format(self.imponibile_operazioni_attive).replace('.', ',')
        # 1.2.2.1.6  TotaleOperazioniPassive
        TotaleOperazioniPassive = etree.SubElement(
            x1_2_2_DatiContabili, 'TotaleOperazioniPassive')
        TotaleOperazioniPassive.text = "{:.2f}"\
            .format(self.imponibile_operazioni_passive).replace('.', ',')
        # 1.2.2.1.7  IvaEsigibile
        IvaEsigibile = etree.SubElement(
            x1_2_2_DatiContabili, 'IvaEsigibile')
        IvaEsigibile.text = "{:.2f}".format(self.iva_esigibile)\
            .replace('.', ',')
        # 1.2.2.1.8  IvaDetratta
        IvaDetratta = etree.SubElement(
            x1_2_2_DatiContabili, 'IvaDetratta')
        IvaDetratta.text = "{:.2f}".format(self.iva_detratta)\
            .replace('.', ',')
        # 1.2.2.1.9  IvaDovuta
        if self.iva_dovuta_debito:
            IvaDovuta = etree.SubElement(
                x1_2_2_DatiContabili, 'IvaDovuta')
            IvaDovuta.text = "{:.2f}".format(self.iva_dovuta_debito)\
                .replace('.', ',')
        # 1.2.2.1.10  IvaCredito
        if self.iva_dovuta_credito:
            IvaCredito = etree.SubElement(
                x1_2_2_DatiContabili, 'IvaCredito')
            IvaCredito.text = "{:.2f}".format(self.iva_dovuta_credito)\
                .replace('.', ',')
        # 1.2.2.1.11 DebitoPrecedente
        DebitoPrecedente = etree.SubElement(
            x1_2_2_DatiContabili, 'DebitoPrecedente')
        DebitoPrecedente.text = "{:.2f}".format(
            self.debito_periodo_precedente).replace('.', ',')
        # 1.2.2.1.12 CreditoPeriodoPrecedente
        CreditoPeriodoPrecedente = etree.SubElement(
            x1_2_2_DatiContabili, 'CreditoPeriodoPrecedente')
        CreditoPeriodoPrecedente.text = "{:.2f}".format(
            self.credito_periodo_precedente).replace('.', ',')
        # 1.2.2.1.13 CreditoAnnoPrecedente
        CreditoAnnoPrecedente = etree.SubElement(
            x1_2_2_DatiContabili, 'CreditoAnnoPrecedente')
        CreditoAnnoPrecedente.text = "{:.2f}".format(
            self.credito_anno_precedente).replace('.', ',')
        # 1.2.2.1.14 VersamentiAutoUE
        VersamentiAutoUE = etree.SubElement(
            x1_2_2_DatiContabili, 'VersamentiAutoUE')
        VersamentiAutoUE.text = "{:.2f}".format(
            self.versamento_auto_UE).replace('.', ',')
        # 1.2.2.1.15 CreditiImposta
        CreditiImposta = etree.SubElement(
            x1_2_2_DatiContabili, 'CreditiImposta')
        CreditiImposta.text = "{:.2f}".format(
            self.crediti_imposta).replace('.', ',')
        # 1.2.2.1.16 InteressiDovuti
        InteressiDovuti = etree.SubElement(
            x1_2_2_DatiContabili, 'InteressiDovuti')
        InteressiDovuti.text = "{:.2f}".format(
            self.interessi_dovuti).replace('.', ',')
        # 1.2.2.1.17 Acconto
        Acconto = etree.SubElement(
            x1_2_2_DatiContabili, 'Acconto')
        Acconto.text = "{:.2f}".format(
            self.accounto_dovuto).replace('.', ',')
        # 1.2.2.1.18 ImportoDaVersare
        ImportoDaVersare = etree.SubElement(
            x1_2_2_DatiContabili, 'ImportoDaVersare')
        ImportoDaVersare.text = "{:.2f}".format(
            self.iva_da_versare).replace('.', ',')
        # 1.2.2.1.19 ImportoACredito
        ImportoACredito = etree.SubElement(
            x1_2_2_DatiContabili, 'ImportoACredito')
        ImportoACredito.text = "{:.2f}".format(
            self.iva_a_credito).replace('.', ',')

        return x1_2_2_DatiContabili
