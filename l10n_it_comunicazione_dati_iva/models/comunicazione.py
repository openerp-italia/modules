# -*- coding: utf-8 -*-


from openerp import api, fields, models, _
from datetime import datetime
from openerp.exceptions import ValidationError


class ComunicazioneDatiIva(models.Model):
    _name = 'comunicazione.dati.iva'
    _description = 'Comunicazione Dati IVA'

    @api.model
    def _default_company(self):
        company_id = self._context.get(
            'company_id', self.env.user.company_id.id)
        return company_id

    @api.constrains('identificativo')
    def _check_identificativo(self):
        domain = [('identificativo', '=', self.identificativo)]
        dichiarazioni = self.search(domain)
        if len(dichiarazioni) > 1:
            raise ValidationError(
                _("Dichiarazione già esiste con identificativo {}"
                  ).format(self.identificativo))

    def _get_identificativo(self):
        dichiarazioni = self.search([])
        if dichiarazioni:
            return len(dichiarazioni) + 1
        else:
            return 1

    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=_default_company)
    identificativo = fields.Integer(string='Identificativo',
                                    default=_get_identificativo)
    name = fields.Char(string='Name', compute="_compute_name")
    declarant_fiscalcode = fields.Char(string='Fiscalcode')
    codice_carica_id = fields.Many2one('codice.carica', string='Codice carica')
    date_start = fields.Date(string='Date start', required=True)
    date_end = fields.Date(string='Date end', required=True)
    fatture_emesse_ids = fields.One2many(
        'comunicazione.dati.iva.fatture.emesse', 'comunicazione_id',
        string='Fatture Emesse')
    fatture_ricevute_ids = fields.One2many(
        'comunicazione.dati.iva.fatture.ricevute', 'comunicazione_id',
        string='Fatture Ricevute')
    fatture_emesse = fields.Boolean(string="Fatture Emesse")
    fatture_ricevute = fields.Boolean(string="Fatture Ricevute")
    annullamento_dati_precedenti = fields.Boolean(string="Annullamento Dati"
                                                         " Precedenti")

    @api.multi
    def _compute_name(self):
        name = ""
        for dich in self:
            """
            for quadro in dich.quadri_vp_ids:
                if not name:
                    name += '{} {}'.format(str(dich.year),
                                           quadro.period_type)
                if quadro.period_type == 'month':
                    name += ', {}'.format(str(quadro.month))
                else:
                    name += ', {}'.format(str(quadro.quarter))"""
            dich.name = name

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            if self.company_id.partner_id.vat:
                self.taxpayer_vat = self.company_id.partner_id.vat[2:]
            else:
                self.taxpayer_vat = ''
            self.taxpayer_fiscalcode = \
                self.company_id.partner_id.fiscalcode

    @api.one
    def compute_values(self):
        # Unlink existing lines
        self._unlink_sections()
        # Fatture Emesse
        fatture_emesse = self._get_fatture_emesse()

    def _get_fatture_emesse(self):
        for comunicazione in self:
            domain = [('fiscal_document_type_id.type', 'in',
                       ['out_invoice', 'out_refund']),
                      ('date_invoice', '>=', comunicazione.date_start),
                      ('date_invoice', '<=', comunicazione.date_end)]
            invoices += self.env['account.invoice'].search(domain)
        return invoices

    def _unlink_sections(self):
        for comunicazione in self:
            comunicazione.fatture_emesse_ids = False

        return True


class ComunicazioneDatiIvaFattureEmesse(models.Model):
    _name = 'comunicazione.dati.iva.fatture.emesse'
    _description = 'Comunicazione Dati IVA - Fatture Emesse'

    comunicazione_id = fields.Many2one(
        'comunicazione.dati.iva', string='Comunicazione', readonly=True)
    partner_company_id = fields.Many2one('res.partner', string='Partner')

    # Cedente
    cedente_IdFiscaleIVA_IdPaese = fields.Char(
        string='Id Paese', size=2, help="Codice della nazione espresso secondo\
         lo standard ISO 3166-1 alpha-2 code")
    cedente_IdFiscaleIVA_IdCodice = fields.Char(
        string='Codice identificativo fiscale', size=28)
    cedente_CodiceFiscale = fields.Char(
        string='Codice Fiscale', size=16)
    cedente_Denominazione = fields.Char(
        string='Ditta, denominazione o ragione sociale', size=80)
    cedente_Nome = fields.Char(
        string='Nome della persona fisica', size=60, help="Obbligatorio ma da\
         valorizzare insieme all'elemento 2.1.2.3 <Cognome>  ed in \
         alternativa all'elemento 2.1.2.1 <Denominazione> ")
    cedente_Cognome = fields.Char(
        string='Cognome della persona fisica', size=60, help="Obbligatorio \
        ma da valorizzare insieme all'elemento 2.1.2.2 <Nome>  ed in \
        alternativa all'elemento 2.1.2.1 <Denominazione>")
    cedente_sede_Indirizzo = fields.Char(
        string='Indirizzo della sede', size=60)
    cedente_sede_NumeroCivico = fields.Char(
        string='Numero civico', size=8)
    cedente_sede_Cap = fields.Char(
        string='Numero civico', size=5)
    cedente_sede_Comune = fields.Char(
        string='Comune', size=60)
    cedente_sede_Provincia = fields.Char(
        string='Provincia', size=2)
    cedente_sede_Nazione = fields.Char(
        string='Nazione', size=2, help="Codice della nazione espresso secondo\
         lo standard ISO 3166-1 alpha-2 code")
    cedente_so_Indirizzo = fields.Char(
        string='Indirizzo della stabile organizzazione in Italia', size=60)
    cedente_so_NumeroCivico = fields.Char(
        string='Numero civico', size=8)
    cedente_so_Cap = fields.Char(
        string='Numero civico', size=5)
    cedente_so_Comune = fields.Char(
        string='Comune', size=60)
    cedente_so_Provincia = fields.Char(
        string='Provincia', size=2)
    cedente_so_Nazione = fields.Char(
        string='Nazione', size=2, help="Codice della nazione espresso secondo\
         lo standard ISO 3166-1 alpha-2 code")
    cedente_rf_IdFiscaleIVA_IdPaese = fields.Char(
        string='Id Paese', size=2, help="Accetta solo IT")
    cedente_rf_IdFiscaleIVA_IdCodice = fields.Char(
        string='Codice identificativo fiscale', size=11)
    cedente_rf_Denominazione = fields.Char(
        string='Ditta, denominazione o ragione sociale', size=80,
        help="Ditta, denominazione o ragione sociale (ditta, impresa, \
        società, ente) del rappresentante fiscale. Obbligatorio ma da \
        valorizzare in alternativa agli elementi 2.1.2.6.3 <Nome>  e  \
        2.1.2.6.4 <Cognome>")
    cedente_rf_Nome = fields.Char(
        string='Nome della persona fisica', size=60, help="Nome del \
        rappresentante fiscale persona fisica Obbligatorio ma da valorizzare\
         insieme all'elemento 2.1.2.6.4 <Cognome>  ed in alternativa \
         all'elemento 2.1.2.6.2 <Denominazione>")
    cedente_rf_Cognome = fields.Char(
        string='Cognome della persona fisica', size=60, help="Cognome del \
        rappresentante fiscale persona fisica. Obbligatorio ma da valorizzare\
         insieme all'elemento 2.1.2.6.3 <Nome>  ed in alternativa \
         all'elemento 2.1.2.6.2 <Denominazione>")

    # Dati Cessionario e Fattura
    fatture_emesse_body_ids = fields.One2many(
        'comunicazione.dati.iva.fatture.emesse.body', 'fattura_emessa_id',
        string='Body Fatture Emesse')

    # Rettifica
    rettifica_IdFile = fields.Char(
        string='Identificativo del file',
        help="Identificativo del file contenente i dati fattura che si vogliono\
         rettificare. E' l'identificativo comunicato dal sistema in fase di \
         trasmissione del file")
    rettifica_Posizione = fields.Integer(
        string='Posizione', help="Posizione della fattura all'interno del \
        file trasmesso")

    @api.onchange('partner_company_id')
    def onchange_partner_company_id(self):
        for fattura in self:
            if fattura.partner_company_id:
                fattura.cedente_IdFiscaleIVA_IdPaese = \
                    fattura.partner_company_id.country_id.code or ''
                fattura.cedente_IdFiscaleIVA_IdCodice = \
                    fattura.partner_company_id.vat[2:] if \
                    fattura.partner_company_id.vat else ''
                fattura.cedente_CodiceFiscale = \
                    fattura.partner_company_id.fiscalcode or ''
                fattura.cedente_Denominazione = \
                    fattura.partner_company_id.name or ''
                # Sede
                fattura.cedente_sede_Indirizzo = '{} {}'.format(
                    fattura.partner_company_id.street,
                    fattura.partner_company_id.street2)
                fattura.cedente_sede_Cap = \
                    fattura.partner_company_id.zip or ''
                fattura.cedente_sede_Comune = \
                    fattura.partner_company_id.city or ''
                fattura.cedente_sede_Provincia = \
                    fattura.partner_company_id.state_id and \
                    fattura.partner_company_id.state_id.code or ''
                fattura.cedente_sede_Nazione = \
                    fattura.partner_company_id.country_id and \
                    fattura.partner_company_id.country_id.code or ''


class ComunicazioneDatiIvaFattureEmesseBody(models.Model):
    _name = 'comunicazione.dati.iva.fatture.emesse.body'
    _description = 'Comunicazione Dati IVA - Body Fatture Emesse'

    fattura_emessa_id = fields.Many2one(
        'comunicazione.dati.iva.fatture.emesse', string="Fattura Emessa")
    partner_id = fields.Many2one('res.partner', string='Partner')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    posizione = fields.Integer(
        "Posizione della fattura all'interno del file trasmesso")
    cessionario_IdFiscaleIVA_IdPaese = fields.Char(
        string='Id Paese', size=2, help="Codice della nazione espresso secondo\
             lo standard ISO 3166-1 alpha-2 code")
    cessionario_IdFiscaleIVA_IdCodice = fields.Char(
        string='Codice identificativo fiscale', size=28)
    cessionario_CodiceFiscale = fields.Char(
        string='Codice Fiscale', size=16)
    cessionario_Denominazione = fields.Char(
        string='Ditta, denominazione o ragione sociale', size=80)
    cessionario_Nome = fields.Char(
        string='Nome della persona fisica', size=60, help="Obbligatorio ma da\
             valorizzare insieme all'elemento 2.1.2.3 <Cognome>  ed in \
             alternativa all'elemento 2.1.2.1 <Denominazione> ")
    cessionario_Cognome = fields.Char(
        string='Cognome della persona fisica', size=60, help="Obbligatorio \
            ma da valorizzare insieme all'elemento 2.1.2.2 <Nome>  ed in \
            alternativa all'elemento 2.1.2.1 <Denominazione>")
    cessionario_sede_Indirizzo = fields.Char(
        string='Indirizzo della sede', size=60)
    cessionario_sede_NumeroCivico = fields.Char(
        string='Numero civico', size=8)
    cessionario_sede_Cap = fields.Char(
        string='Numero civico', size=5)
    cessionario_sede_Comune = fields.Char(
        string='Comune', size=60)
    cessionario_sede_Provincia = fields.Char(
        string='Provincia', size=2)
    cessionario_sede_Nazione = fields.Char(
        string='Nazione', size=2, help="Codice della nazione espresso secondo\
             lo standard ISO 3166-1 alpha-2 code")
    cessionario_so_Indirizzo = fields.Char(
        string='Indirizzo della stabile organizzazione in Italia', size=60)
    cessionario_so_NumeroCivico = fields.Char(
        string='Numero civico', size=8)
    cessionario_so_Cap = fields.Char(
        string='Numero civico', size=5)
    cessionario_so_Comune = fields.Char(
        string='Comune', size=60)
    cessionario_so_Provincia = fields.Char(
        string='Provincia', size=2)
    cessionario_so_Nazione = fields.Char(
        string='Nazione', size=2, help="Codice della nazione espresso secondo\
             lo standard ISO 3166-1 alpha-2 code")
    cessionario_rf_IdFiscaleIVA_IdPaese = fields.Char(
        string='Id Paese', size=2, help="Accetta solo IT")
    cessionario_rf_IdFiscaleIVA_IdCodice = fields.Char(
        string='Codice identificativo fiscale', size=11)
    cessionario_rf_Denominazione = fields.Char(
        string='Ditta, denominazione o ragione sociale', size=80,
        help="Ditta, denominazione o ragione sociale (ditta, impresa, \
            società, ente) del rappresentante fiscale. Obbligatorio ma da \
            valorizzare in alternativa agli elementi 2.1.2.6.3 <Nome>  e  \
            2.1.2.6.4 <Cognome>")
    cessionario_rf_Nome = fields.Char(
        string='Nome della persona fisica', size=60, help="Nome del \
            rappresentante fiscale persona fisica Obbligatorio ma da valorizzare\
             insieme all'elemento 2.1.2.6.4 <Cognome>  ed in alternativa \
             all'elemento 2.1.2.6.2 <Denominazione>")
    cessionario_rf_Cognome = fields.Char(
        string='Cognome della persona fisica', size=60, help="Cognome del \
            rappresentante fiscale persona fisica. Obbligatorio ma da valorizzare\
             insieme all'elemento 2.1.2.6.3 <Nome>  ed in alternativa \
             all'elemento 2.1.2.6.2 <Denominazione>")
    dati_fattura_TipoDocumento = fields.Many2one(
        'fiscal.document.type', string='Tipo Documento', required=True)
    dati_fattura_Data = fields.Date(string='Data Documento', required=True)
    dati_fattura_Numero = fields.Char(string='Numero Documento', required=True)
    dati_fattura_iva_ids = fields.One2many(
        'comunicazione.dati.iva.fatture.emesse.iva', 'fattura_emessa_body_id',
        string='Riepilogo Iva')

    @api.onchange('invoice_id')
    def onchange_invoice_id(self):
        for fattura in self:
            if fattura.invoice_id:
                fattura.dati_fattura_TipoDocumento = \
                    fattura.invoice_id.fiscal_document_type_id and \
                    fattura.invoice_id.fiscal_document_type_id.id or False
                fattura.dati_fattura_Numero = fattura.invoice_id.number
                fattura.dati_fattura_Data = fattura.invoice_id.date_invoice
                fattura.partner_id = fattura.invoice_id.partner_id.id
                fattura.partner_company_id = \
                    fattura.invoice_id.company_id.partner_id.id
                # tax
                tax_lines = []
                for tax_line in fattura.invoice_id.tax_line:
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
                fattura.dati_fattura_iva_ids = tax_lines

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for fattura in self:
            if fattura.partner_id:
                fattura.cessionario_IdFiscaleIVA_IdPaese = \
                    fattura.partner_id.country_id.code or ''
                fattura.cessionario_IdFiscaleIVA_IdCodice = \
                    fattura.partner_id.vat[2:] if fattura.partner_id.vat \
                    else ''
                fattura.cessionario_CodiceFiscale = \
                    fattura.partner_id.fiscalcode or ''
                fattura.cessionario_Denominazione = \
                    fattura.partner_id.name or ''
                # Sede
                fattura.cessionario_sede_Indirizzo = '{} {}'.format(
                    fattura.partner_id.street, fattura.partner_id.street2)
                fattura.cessionario_sede_Cap = \
                    fattura.partner_id.zip or ''
                fattura.cessionario_sede_Comune = \
                    fattura.partner_id.city or ''
                fattura.cessionario_sede_Provincia = \
                    fattura.partner_id.state_id and \
                    fattura.partner_id.state_id.code or ''
                fattura.cessionario_sede_Nazione = \
                    fattura.partner_id.country_id and \
                    fattura.partner_id.country_id.code or ''


class ComunicazioneDatiIvaFattureEmesseIva(models.Model):
    _name = 'comunicazione.dati.iva.fatture.emesse.iva'
    _description = 'Comunicazione Dati IVA - Fatture Emesse Iva'

    fattura_emessa_body_id = fields.Many2one(
        'comunicazione.dati.iva.fatture.emesse.body',
        string='Body Fattura Emessa', readonly=True)
    ImponibileImporto = fields.Float(
        string='Base imponibile', help="Ammontare (base) imponibile ( per le\
         operazioni soggette ad IVA )  o importo non imponibile (per le \
         operazioni per le quali il cedente/prestatore [FORNITORE] non deve \
         indicare l'imposta in fattura ) o somma di imponibile e imposta \
         (per le operazioni soggette ai regimi che prevedono questa \
         rappresentazione). Per le fatture SEMPLIFICATE  (elemento 2.2.3.1.1 \
         <TipoDocumento>  =  'TD07'  o 'TD08'), ospita l'importo risultante\
          dalla somma di imponibile ed imposta")
    Imposta = fields.Float(
        string='Imposta', help="Se l'elemento 2.2.3.1.1 \
        <TipoDocumento> vale 'TD07' o 'TD08' (fattura semplificata), si può \
        indicare in alternativa all'elemento 2.2.3.2.2.2 <Aliquota>. Per tutti\
         gli altri valori dell'elemento 2.2.3.1.1 <TipoDocumento> deve essere\
          valorizzato.")
    Aliquota = fields.Float(
        string='Aliquota', help="Aliquota IVA, espressa in percentuale\
         (da valorizzare a 0.00 nel caso di operazioni per le quali il \
         cedente/prestatore [FORNITORE] non deve indicare l'imposta in fattura\
         ). Se l'elemento 2.2.3.1.1 <TipoDocumento> vale 'TD07' o 'TD08' \
         (fattura semplificata), si può indicare in alternativa all'elemento \
         2.2.3.2.2.1 <Imposta>. Per tutti gli altri valori dell'elemento \
         2.2.3.1.1 <TipoDocumento> deve essere valorizzata.")
    Natura_id = fields.Char('Natura DA FARE M2O')
    Detraibile = fields.Float(string='Detraibile %')
    Deducibile = fields.Char(string='Deducibile', size=2,
                             help="valori ammessi: [SI] = spesa deducibile")
    EsigibilitaIVA = fields.Selection(
        [('I', 'Immediata'), ('D', 'Differita'),
         ('S', 'Scissione dei pagamenti')], string='Esigibilità IVA')


class ComunicazioneDatiIvaFattureRicevute(models.Model):
    _name = 'comunicazione.dati.iva.fatture.ricevute'
    _description = 'Comunicazione Dati IVA - Fatture Ricevute'

    comunicazione_id = fields.Many2one(
        'comunicazione.dati.iva', string='Comunicazione', readonly=True)
    partner_company_id = fields.Many2one('res.partner', string='Partner')

    # Cessionario
    cessionario_IdFiscaleIVA_IdPaese = fields.Char(
        string='Id Paese', size=2, help="Codice della nazione espresso secondo\
         lo standard ISO 3166-1 alpha-2 code")
    cessionario_IdFiscaleIVA_IdCodice = fields.Char(
        string='Codice identificativo fiscale', size=28)
    cessionario_CodiceFiscale = fields.Char(
        string='Codice Fiscale', size=16)
    cessionario_Denominazione = fields.Char(
        string='Ditta, denominazione o ragione sociale', size=80)
    cessionario_Nome = fields.Char(
        string='Nome della persona fisica', size=60, help="Obbligatorio ma da\
         valorizzare insieme all'elemento 3.1.2.3 <Cognome>  ed in \
         alternativa all'elemento 3.1.2.1 <Denominazione> ")
    cessionario_Cognome = fields.Char(
        string='Cognome della persona fisica', size=60, help="Obbligatorio \
        ma da valorizzare insieme all'elemento 3.1.2.2 <Nome>  ed in \
        alternativa all'elemento 3.1.2.1 <Denominazione>")
    cessionario_sede_Indirizzo = fields.Char(
        string='Indirizzo della sede', size=60)
    cessionario_sede_NumeroCivico = fields.Char(
        string='Numero civico', size=8)
    cessionario_sede_Cap = fields.Char(
        string='CAP', size=5)
    cessionario_sede_Comune = fields.Char(
        string='Comune', size=60)
    cessionario_sede_Provincia = fields.Char(
        string='Provincia', size=2)
    cessionario_sede_Nazione = fields.Char(
        string='Nazione', size=2, help="Codice della nazione espresso secondo\
         lo standard ISO 3166-1 alpha-2 code")
    cessionario_so_Indirizzo = fields.Char(
        string='Indirizzo della stabile organizzazione in Italia', size=60)
    cessionario_so_NumeroCivico = fields.Char(
        string='Numero civico', size=8)
    cessionario_so_Cap = fields.Char(
        string='Numero civico', size=5)
    cessionario_so_Comune = fields.Char(
        string='Comune', size=60)
    cessionario_so_Provincia = fields.Char(
        string='Provincia', size=2)
    cessionario_so_Nazione = fields.Char(
        string='Nazione', size=2, help="Codice della nazione espresso secondo\
         lo standard ISO 3166-1 alpha-2 code")
    cessionario_rf_IdFiscaleIVA_IdPaese = fields.Char(
        string='Id Paese', size=2, help="Accetta solo IT")
    cessionario_rf_IdFiscaleIVA_IdCodice = fields.Char(
        string='Codice identificativo fiscale', size=11)
    cessionario_rf_Denominazione = fields.Char(
        string='Ditta, denominazione o ragione sociale', size=80,
        help="Ditta, denominazione o ragione sociale (ditta, impresa, \
        società, ente) del rappresentante fiscale. Obbligatorio ma da \
        valorizzare in alternativa agli elementi 3.1.2.6.3 <Nome>  e  \
        3.1.2.6.4 <Cognome>")
    cessionario_rf_Nome = fields.Char(
        string='Nome della persona fisica', size=60, help="Nome del \
        rappresentante fiscale persona fisica Obbligatorio ma da valorizzare\
         insieme all'elemento 3.1.2.6.4 <Cognome>  ed in alternativa \
         all'elemento 3.1.2.6.2 <Denominazione>")
    cessionario_rf_Cognome = fields.Char(
        string='Cognome della persona fisica', size=60, help="Cognome del \
        rappresentante fiscale persona fisica. Obbligatorio ma da valorizzare\
         insieme all'elemento 3.1.2.6.3 <Nome>  ed in alternativa \
         all'elemento 3.1.2.6.2 <Denominazione>")

    # Dati Cedente e Fattura
    fatture_ricevute_body_ids = fields.One2many(
        'comunicazione.dati.iva.fatture.ricevute.body', 'fattura_ricevuta_id',
        string='Body Fatture Ricevute')

    # Rettifica
    rettifica_IdFile = fields.Char(
        string='Identificativo del file',
        help="Identificativo del file contenente i dati fattura che si vogliono\
         rettificare. E' l'identificativo comunicato dal sistema in fase di \
         trasmissione del file")
    rettifica_Posizione = fields.Integer(
        string='Posizione', help="Posizione della fattura all'interno del \
        file trasmesso")

    @api.onchange('partner_company_id')
    def onchange_partner_company_id(self):
        for fattura in self:
            if fattura.partner_company_id:
                fattura.cessionario_IdFiscaleIVA_IdPaese = \
                    fattura.partner_company_id.country_id.code or ''
                fattura.cessionario_IdFiscaleIVA_IdCodice = \
                    fattura.partner_company_id.vat[2:] if \
                        fattura.partner_company_id.vat else ''
                fattura.cessionario_CodiceFiscale = \
                    fattura.partner_company_id.fiscalcode or ''
                fattura.cessionario_Denominazione = \
                    fattura.partner_company_id.name or ''
                # Sede
                fattura.cessionario_sede_Indirizzo = '{} {}'.format(
                    fattura.partner_company_id.street,
                    fattura.partner_company_id.street2)
                fattura.cessionario_sede_Cap = \
                    fattura.partner_company_id.zip or ''
                fattura.cessionario_sede_Comune = \
                    fattura.partner_company_id.city or ''
                fattura.cessionario_sede_Provincia = \
                    fattura.partner_company_id.state_id and \
                    fattura.partner_company_id.state_id.code or ''
                fattura.cessionario_sede_Nazione = \
                    fattura.partner_company_id.country_id and \
                    fattura.partner_company_id.country_id.code or ''


class ComunicazioneDatiIvaFattureRicevuteBody(models.Model):
    _name = 'comunicazione.dati.iva.fatture.ricevute.body'
    _description = 'Comunicazione Dati IVA - Body Fatture Ricevute'

    fattura_ricevuta_id = fields.Many2one(
        'comunicazione.dati.iva.fatture.ricevute', string="Fattura Ricevuta")
    posizione = fields.Integer(
        "Posizione della fattura all'interno del file trasmesso")
    partner_id = fields.Many2one('res.partner', string='Partner')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    cedente_IdFiscaleIVA_IdPaese = fields.Char(
        string='Id Paese', size=2, help="Codice della nazione espresso secondo\
             lo standard ISO 3166-1 alpha-2 code")
    cedente_IdFiscaleIVA_IdCodice = fields.Char(
        string='Codice identificativo fiscale', size=28)
    cedente_CodiceFiscale = fields.Char(
        string='Codice Fiscale', size=16)
    cedente_Denominazione = fields.Char(
        string='Ditta, denominazione o ragione sociale', size=80)
    cedente_Nome = fields.Char(
        string='Nome della persona fisica', size=60, help="Obbligatorio ma da\
             valorizzare insieme all'elemento 3.2.2.3 <Cognome>  ed in \
             alternativa all'elemento 3.2.2.1 <Denominazione> ")
    cedente_Cognome = fields.Char(
        string='Cognome della persona fisica', size=60, help="Obbligatorio \
            ma da valorizzare insieme all'elemento 3.2.2.2 <Nome>  ed in \
            alternativa all'elemento 3.2.2.1 <Denominazione>")
    cedente_sede_Indirizzo = fields.Char(
        string='Indirizzo della sede', size=60)
    cedente_sede_NumeroCivico = fields.Char(
        string='Numero civico', size=8)
    cedente_sede_Cap = fields.Char(
        string='Numero civico', size=5)
    cedente_sede_Comune = fields.Char(
        string='Comune', size=60)
    cedente_sede_Provincia = fields.Char(
        string='Provincia', size=2)
    cedente_sede_Nazione = fields.Char(
        string='Nazione', size=2, help="Codice della nazione espresso secondo\
             lo standard ISO 3166-1 alpha-2 code")
    cedente_so_Indirizzo = fields.Char(
        string='Indirizzo della stabile organizzazione in Italia', size=60)
    cedente_so_NumeroCivico = fields.Char(
        string='Numero civico', size=8)
    cedente_so_Cap = fields.Char(
        string='Numero civico', size=5)
    cedente_so_Comune = fields.Char(
        string='Comune', size=60)
    cedente_so_Provincia = fields.Char(
        string='Provincia', size=2)
    cedente_so_Nazione = fields.Char(
        string='Nazione', size=2, help="Codice della nazione espresso secondo\
             lo standard ISO 3166-1 alpha-2 code")
    cedente_rf_IdFiscaleIVA_IdPaese = fields.Char(
        string='Id Paese', size=2, help="Accetta solo IT")
    cedente_rf_IdFiscaleIVA_IdCodice = fields.Char(
        string='Codice identificativo fiscale', size=11)
    cedente_rf_Denominazione = fields.Char(
        string='Ditta, denominazione o ragione sociale', size=80,
        help="Ditta, denominazione o ragione sociale (ditta, impresa, \
            società, ente) del rappresentante fiscale. Obbligatorio ma da \
            valorizzare in alternativa agli elementi 3.2.2.6.3 <Nome>  e  \
            3.2.2.6.4 <Cognome>")
    cedente_rf_Nome = fields.Char(
        string='Nome della persona fisica', size=60, help="Nome del \
            rappresentante fiscale persona fisica Obbligatorio ma da valorizzare\
             insieme all'elemento 3.2.2.6.4 <Cognome>  ed in alternativa \
             all'elemento 3.2.2.6.2 <Denominazione>")
    cedente_rf_Cognome = fields.Char(
        string='Cognome della persona fisica', size=60, help="Cognome del \
            rappresentante fiscale persona fisica. Obbligatorio ma da valorizzare\
             insieme all'elemento 3.2.2.6.3 <Nome>  ed in alternativa \
             all'elemento 3.2.2.6.2 <Denominazione>")
    dati_fattura_TipoDocumento = fields.Many2one(
        'fiscal.document.type', string='Tipo Documento', required=True)
    dati_fattura_Data = fields.Date(string='Data Documento', required=True)
    dati_fattura_Numero = fields.Char(string='Numero Documento', required=True)
    dati_fattura_iva_ids = fields.One2many(
        'comunicazione.dati.iva.fatture.ricevute.iva', 'fattura_ricevuta_body_id',
        string='Riepilogo Iva')

    @api.onchange('invoice_id')
    def onchange_invoice_id(self):
        for fattura in self:
            if fattura.invoice_id:
                fattura.dati_fattura_TipoDocumento = \
                    fattura.invoice_id.fiscal_document_type_id and \
                    fattura.invoice_id.fiscal_document_type_id.id or False
                fattura.dati_fattura_Numero = fattura.invoice_id.number
                fattura.dati_fattura_Data = fattura.invoice_id.date_invoice
                fattura.partner_id = fattura.invoice_id.partner_id.id
                fattura.partner_company_id = \
                    fattura.invoice_id.company_id.partner_id.id
                # tax
                tax_lines = []
                for tax_line in fattura.invoice_id.tax_line:
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
                fattura.dati_fattura_iva_ids = tax_lines

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for fattura in self:
            if fattura.partner_id:
                fattura.cedente_IdFiscaleIVA_IdPaese = \
                    fattura.partner_id.country_id.code or ''
                fattura.cedente_IdFiscaleIVA_IdCodice = \
                    fattura.partner_id.vat[2:] if fattura.partner_id.vat \
                        else ''
                fattura.cedente_CodiceFiscale = \
                    fattura.partner_id.fiscalcode or ''
                fattura.cedente_Denominazione = \
                    fattura.partner_id.name or ''
                # Sede
                fattura.cedente_sede_Indirizzo = '{} {}'.format(
                    fattura.partner_id.street, fattura.partner_id.street2)
                fattura.cedente_sede_Cap = \
                    fattura.partner_id.zip or ''
                fattura.cedente_sede_Comune = \
                    fattura.partner_id.city or ''
                fattura.cedente_sede_Provincia = \
                    fattura.partner_id.state_id and \
                    fattura.partner_id.state_id.code or ''
                fattura.cedente_sede_Nazione = \
                    fattura.partner_id.country_id and \
                    fattura.partner_id.country_id.code or ''


class ComunicazioneDatiIvaFattureRicevuteIva(models.Model):
    _name = 'comunicazione.dati.iva.fatture.ricevute.iva'
    _description = 'Comunicazione Dati IVA - Fatture Ricevute Iva'

    fattura_ricevuta_body_id = fields.Many2one(
        'comunicazione.dati.iva.fatture.ricevute.body',
        string='Body Fattura Ricevuta', readonly=True)
    ImponibileImporto = fields.Float(
        string='Base imponibile', help="Ammontare (base) imponibile ( per le\
         operazioni soggette ad IVA )  o importo non imponibile (per le \
         operazioni per le quali il cedente/prestatore [FORNITORE] non deve \
         indicare l'imposta in fattura ) o somma di imponibile e imposta \
         (per le operazioni soggette ai regimi che prevedono questa \
         rappresentazione). Per le fatture SEMPLIFICATE  (elemento 3.2.3.1.1 \
         <TipoDocumento>  =  'TD07'  o 'TD08'), ospita l'importo risultante\
          dalla somma di imponibile ed imposta")
    Imposta = fields.Float(
        string='Imposta', help="Se l'elemento 3.2.3.1.1 \
        <TipoDocumento> vale 'TD07' o 'TD08' (fattura semplificata), si può \
        indicare in alternativa all'elemento 3.2.3.2.2.2 <Aliquota>. Per tutti\
         gli altri valori dell'elemento 3.2.3.1.1 <TipoDocumento> deve essere\
          valorizzato.")
    Aliquota = fields.Float(
        string='Aliquota', help="Aliquota IVA, espressa in percentuale\
         (da valorizzare a 0.00 nel caso di operazioni per le quali il \
         cedente/prestatore [FORNITORE] non deve indicare l'imposta in fattura\
         ). Se l'elemento 3.2.3.1.1 <TipoDocumento> vale 'TD07' o 'TD08' \
         (fattura semplificata), si può indicare in alternativa all'elemento \
         3.2.3.2.2.1 <Imposta>. Per tutti gli altri valori dell'elemento \
         3.2.3.1.1 <TipoDocumento> deve essere valorizzata.")
    Natura_id = fields.Char('Natura DA FARE M2O')
    Detraibile = fields.Float(string='Detraibile %')
    Deducibile = fields.Char(string='Deducibile', size=2,
                             help="valori ammessi: [SI] = spesa deducibile")
    EsigibilitaIVA = fields.Selection([('I', 'Immediata'),
                                       ('D', 'Differita'),
                                       ('S', 'Scissione dei pagamenti')],
                                      string='Esigibilità IVA')
