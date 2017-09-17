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
    # Cedente
    partner_cedente_id = fields.Many2one('res.partner', string='Partner')
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
    # Cessionario
    partner_cessionario_id = fields.Many2one('res.partner', string='Partner')
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

    @api.onchange('partner_cedente_id')
    def onchange_partner_cedente_id(self):
        for comunicazione in self:
            if comunicazione.partner_cedente_id:
                vals = self._prepare_cedente_partner_id(
                    comunicazione.partner_cedente_id)
                comunicazione.cedente_IdFiscaleIVA_IdPaese = \
                    vals['cedente_IdFiscaleIVA_IdPaese']
                comunicazione.cedente_IdFiscaleIVA_IdCodice = \
                    vals['cedente_IdFiscaleIVA_IdCodice']
                comunicazione.cedente_CodiceFiscale = \
                    vals['cedente_CodiceFiscale']
                comunicazione.cedente_Denominazione = \
                    vals['cedente_Denominazione']
                # Sede
                comunicazione.cedente_sede_Indirizzo =\
                    vals['cedente_sede_Indirizzo']
                comunicazione.cessionario_sede_Cap = \
                    vals['cedente_sede_Cap']
                comunicazione.cedente_sede_Comune = \
                    vals['cedente_sede_Comune']
                comunicazione.cedente_sede_Provincia = \
                    vals['cedente_sede_Provincia']
                comunicazione.cedente_sede_Nazione = \
                    vals['cedente_sede_Nazione']

    def _prepare_cedente_partner_id(self, partner, vals=None):
        vals = {}
        vals['cedente_IdFiscaleIVA_IdPaese'] = \
            partner.country_id.code or ''
        vals['cedente_IdFiscaleIVA_IdCodice'] = \
            partner.vat[2:] if partner.vat else ''
        vals['cedente_CodiceFiscale'] = partner.fiscalcode or ''
        vals['cedente_Denominazione'] = partner.name or ''
        # Sede
        vals['cedente_sede_Indirizzo'] = '{} {}'.format(
            partner.street or '', partner.street2 or '')
        vals['cedente_sede_Cap'] = partner.zip or ''
        vals['cedente_sede_Comune'] = partner.city or ''
        vals['cedente_sede_Provincia'] = partner.state_id and \
            partner.state_id.code or ''
        vals['cedente_sede_Nazione'] = partner.country_id and \
            partner.country_id.code or ''
        return vals

    @api.multi
    @api.onchange('partner_cessionario_id')
    def onchange_partner_cessionario_id(self):
        for comunicazione in self:
            if comunicazione.partner_cessionario_id:
                vals = self._prepare_cessionario_partner_id(
                    comunicazione.partner_cessionario_id)
                comunicazione.cessionario_IdFiscaleIVA_IdPaese = \
                    vals['cessionario_IdFiscaleIVA_IdPaese']
                fattucomunicazionera.cessionario_IdFiscaleIVA_IdCodice = \
                    vals['cessionario_IdFiscaleIVA_IdCodice']
                comunicazione.cessionario_CodiceFiscale = \
                    vals['cessionario_CodiceFiscale']
                comunicazione.cessionario_Denominazione = \
                    vals['cessionario_Denominazione']
                # Sede
                comunicazione.cessionario_sede_Indirizzo =\
                    vals['cessionario_sede_Indirizzo']
                comunicazione.cessionario_sede_Cap = \
                    vals['cessionario_sede_Cap']
                comunicazione.cessionario_sede_Comune = \
                    vals['cessionario_sede_Comune']
                comunicazione.cessionario_sede_Provincia = \
                    vals['cessionario_sede_Provincia']
                comunicazione.cessionario_sede_Nazione = \
                    vals['cessionario_sede_Nazione']

    def _prepare_cessionario_partner_id(self, partner, vals=None):
        vals = {}
        vals['cessionario_IdFiscaleIVA_IdPaese'] = \
            partner.country_id.code or ''
        vals['cessionario_IdFiscaleIVA_IdCodice'] = \
            partner.vat[2:] if partner.vat else ''
        vals['cessionario_CodiceFiscale'] = partner.fiscalcode or ''
        vals['cessionario_Denominazione'] = partner.name or ''
        # Sede
        vals['cessionario_sede_Indirizzo'] = '{} {}'.format(
            partner.street or '', partner.street2 or '')
        vals['cessionario_sede_Cap'] = partner.zip or ''
        vals['cessionario_sede_Comune'] = partner.city or ''
        vals['cessionario_sede_Provincia'] = partner.state_id and \
            partner.state_id.code or ''
        vals['cessionario_sede_Nazione'] = partner.country_id and \
            partner.country_id.code or ''
        return vals

    def _prepare_fattura_emessa(self, vals, fattura):
        return vals

    def _prepare_fattura_ricevuta(self, vals, fattura):
        return vals

    @api.multi
    def compute_values(self):
        # Unlink existing lines
        self._unlink_sections()
        for comunicazione in self:
            # Fatture Emesse
            if comunicazione.fatture_emesse:
                comunicazione.compute_fatture_emesse()

    @api.one
    def compute_fatture_emesse(self):
        fatture_emesse = self._get_fatture_emesse()
        if fatture_emesse:
            dati_fatture = []
            # Cedente
            self.partner_cedente_id = \
                fatture_emesse[0].company_id.partner_id.id
            self.onchange_partner_cedente_id()

            # Cessionari
            cessionari = fatture_emesse.mapped('partner_id')
            for cessionario in cessionari:
                # Fatture
                fatture = fatture_emesse.filtered(
                    lambda fatture_emesse:
                    fatture_emesse.partner_id.id ==
                        cessionario.id)
                vals_fatture = []
                for fattura in fatture:
                    val = {
                        'invoice_id': fattura.id,
                        'dati_fattura_TipoDocumento':
                            fattura.fiscal_document_type_id.id,
                        'dati_fattura_Data': fattura.date_invoice,
                        'dati_fattura_Numero': fattura.number,
                        'dati_fattura_iva_ids':
                            fattura._get_tax_comunicazione_dati_iva()
                    }
                    val = self._prepare_fattura_emessa(val, fattura)
                    vals_fatture.append((0, 0, val))

                val_cessionario = {
                    'partner_id': cessionario.id,
                    'fatture_emesse_body_ids': vals_fatture
                }
                vals = self._prepare_cessionario_partner_id(
                    cessionario)
                val_cessionario.update(vals)
                dati_fatture.append((0, 0, val_cessionario))
            self.fatture_emesse_ids = dati_fatture

    def _get_fatture_emesse(self):
        invoices = False
        for comunicazione in self:
            domain = [('fiscal_document_type_id.type', 'in',
                       ['out_invoice', 'out_refund']),
                      ('company_id', '>=', comunicazione.company_id.id),
                      ('date_invoice', '>=', comunicazione.date_start),
                      ('date_invoice', '<=', comunicazione.date_end)]
            invoices = self.env['account.invoice'].search(domain)
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
    # Cedente
    partner_id = fields.Many2one('res.partner', string='Partner')
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

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for fattura in self:
            if fattura.partner_id:
                vals = fattura.comunicazione_id.\
                    _prepare_cessionario_partner_id(fattura.partner_id)
                fattura.cessionario_IdFiscaleIVA_IdPaese = \
                    vals['cessionario_IdFiscaleIVA_IdPaese']
                fattura.cessionario_IdFiscaleIVA_IdCodice = \
                    vals['cessionario_IdFiscaleIVA_IdCodice']
                fattura.cessionario_CodiceFiscale = \
                    vals['cessionario_CodiceFiscale']
                fattura.cessionario_Denominazione = \
                    vals['cessionario_Denominazione']
                # Sede
                fattura.cessionario_sede_Indirizzo =\
                    vals['cessionario_sede_Indirizzo']
                fattura.cessionario_sede_Cap = \
                    vals['cessionario_sede_Cap']
                fattura.cessionario_sede_Comune = \
                    vals['cessionario_sede_Comune']
                fattura.cessionario_sede_Provincia = \
                    vals['cessionario_sede_Provincia']
                fattura.cessionario_sede_Nazione = \
                    vals['cessionario_sede_Nazione']


class ComunicazioneDatiIvaFattureEmesseBody(models.Model):
    _name = 'comunicazione.dati.iva.fatture.emesse.body'
    _description = 'Comunicazione Dati IVA - Body Fatture Emesse'

    @api.depends('dati_fattura_iva_ids.ImponibileImporto',
                 'dati_fattura_iva_ids.Imposta')
    def _compute_total(self):
        for ft in self:
            totale_imponibile = 0
            totale_iva = 0
            for tax_line in ft.dati_fattura_iva_ids:
                totale_imponibile += tax_line.ImponibileImporto
                totale_iva += tax_line.Imposta
            ft.totale_imponibile = totale_imponibile
            ft.totale_iva = totale_iva

    fattura_emessa_id = fields.Many2one(
        'comunicazione.dati.iva.fatture.emesse', string="Fattura Emessa")
    posizione = fields.Integer(
        "Posizione della fattura all'interno del file trasmesso")
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    dati_fattura_TipoDocumento = fields.Many2one(
        'fiscal.document.type', string='Tipo Documento', required=True)
    dati_fattura_Data = fields.Date(string='Data Documento', required=True)
    dati_fattura_Numero = fields.Char(string='Numero Documento', required=True)
    dati_fattura_iva_ids = fields.One2many(
        'comunicazione.dati.iva.fatture.emesse.iva', 'fattura_emessa_body_id',
        string='Riepilogo Iva')
    totale_imponibile = fields.Float('Totale Imponibile',
                                     compute="_compute_total", store=True)
    totale_iva = fields.Float('Totale IVA',
                              compute="_compute_total", store=True)

    @api.onchange('invoice_id')
    def onchange_invoice_id(self):
        for fattura in self:
            if fattura.invoice_id:
                fattura.dati_fattura_TipoDocumento = \
                    fattura.invoice_id.fiscal_document_type_id and \
                    fattura.invoice_id.fiscal_document_type_id.id or False
                fattura.dati_fattura_Numero = fattura.invoice_id.number
                fattura.dati_fattura_Data = fattura.invoice_id.date_invoice
                fattura.dati_fattura_iva_ids = \
                    fattura.invoice_id._get_tax_comunicazione_dati_iva()


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
    Natura_id = fields.Many2one('account.tax.kind', string='Natura')
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
    # Cessionario
    partner_id = fields.Many2one('res.partner', string='Partner')
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


class ComunicazioneDatiIvaFattureRicevuteBody(models.Model):
    _name = 'comunicazione.dati.iva.fatture.ricevute.body'
    _description = 'Comunicazione Dati IVA - Body Fatture Ricevute'

    @api.depends('dati_fattura_iva_ids.ImponibileImporto',
                 'dati_fattura_iva_ids.Imposta')
    def _compute_total(self):
        for ft in self:
            totale_imponibile = 0
            totale_iva = 0
            for tax_line in ft.dati_fattura_iva_ids:
                totale_imponibile += tax_line.ImponibileImporto
                totale_iva += tax_line.Imposta
            ft.totale_imponibile = totale_imponibile
            ft.totale_iva = totale_iva

    fattura_ricevuta_id = fields.Many2one(
        'comunicazione.dati.iva.fatture.ricevute', string="Fattura Ricevuta")
    posizione = fields.Integer(
        "Posizione della fattura all'interno del file trasmesso")
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    dati_fattura_TipoDocumento = fields.Many2one(
        'fiscal.document.type', string='Tipo Documento', required=True)
    dati_fattura_Data = fields.Date(string='Data Documento', required=True)
    dati_fattura_Numero = fields.Char(string='Numero Documento', required=True)
    dati_fattura_iva_ids = fields.One2many(
        'comunicazione.dati.iva.fatture.ricevute.iva',
        'fattura_ricevuta_body_id',
        string='Riepilogo Iva')
    totale_imponibile = fields.Float('Totale Imponibile',
                                     compute="_compute_total", store=True)
    totale_iva = fields.Float('Totale IVA',
                              compute="_compute_total", store=True)

    @api.onchange('invoice_id')
    def onchange_invoice_id(self):
        for fattura in self:
            if fattura.invoice_id:
                fattura.dati_fattura_TipoDocumento = \
                    fattura.invoice_id.fiscal_document_type_id and \
                    fattura.invoice_id.fiscal_document_type_id.id or False
                fattura.dati_fattura_Numero = fattura.invoice_id.number
                fattura.dati_fattura_Data = fattura.invoice_id.date_invoice
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
    Natura_id = fields.Char('Natura')
    Detraibile = fields.Float(string='Detraibile %')
    Deducibile = fields.Char(string='Deducibile', size=2,
                             help="valori ammessi: [SI] = spesa deducibile")
    EsigibilitaIVA = fields.Selection([('I', 'Immediata'),
                                       ('D', 'Differita'),
                                       ('S', 'Scissione dei pagamenti')],
                                      string='Esigibilità IVA')
