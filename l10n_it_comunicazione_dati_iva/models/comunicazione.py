# -*- coding: utf-8 -*-


from openerp import api, fields, models, _
from datetime import datetime
from openerp.exceptions import ValidationError
from lxml import etree


NS_IV = 'urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp'
NS_XSI = 'http://www.w3.org/2001/XMLSchema-instance'
NS_LOCATION = 'urn:www.agenziaentrate.gov.it:specificheTecniche:sco:ivp'
NS_MAP = {
    'iv': NS_IV,
    'xsi': NS_XSI,
    #'schemaLocation': NS_LOCATION
}
etree.register_namespace("vi", NS_IV)


def format_decimal(value=0.0):
    return "{:.2f}".format(value).replace('.', ',')


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
    dati_trasmissione = fields.Selection(
        [('DTE', 'Fatture Emesse'), ('DTR', 'Fatture Ricevute'),
         ('ANN', 'Annullamento dai inviati in precedenza')],
        string='Trasmissione dati', required=True)
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
                comunicazione.cessionario_IdFiscaleIVA_IdCodice = \
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
            if comunicazione.dati_trasmissione == 'DTE':
                comunicazione.compute_fatture_emesse()
            # Fatture Ricevute
            if comunicazione.dati_trasmissione == 'DTR':
                comunicazione.compute_fatture_ricevute()

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
            posizione = 0
            cessionari = fatture_emesse.mapped('partner_id')
            for cessionario in cessionari:
                # Fatture
                fatture = fatture_emesse.filtered(
                    lambda fatture_emesse:
                    fatture_emesse.partner_id.id ==
                        cessionario.id)
                vals_fatture = []
                for fattura in fatture:
                    posizione += 1
                    val = {
                        'posizione': posizione,
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

    @api.one
    def compute_fatture_ricevute(self):
        fatture_ricevute = self._get_fatture_ricevute()
        if fatture_ricevute:
            dati_fatture = []
            # Cedente
            self.partner_cessionario_id = \
                fatture_ricevute[0].company_id.partner_id.id
            self.onchange_partner_cessionario_id()

            # Cedenti
            posizione = 0
            cedenti = fatture_ricevute.mapped('partner_id')
            for cedente in cedenti:
                # Fatture
                fatture = fatture_ricevute.filtered(
                    lambda fatture_ricevute:
                    fatture_ricevute.partner_id.id ==
                        cedente.id)
                vals_fatture = []
                for fattura in fatture:
                    posizione += 1
                    val = {
                        'posizione': posizione,
                        'invoice_id': fattura.id,
                        'dati_fattura_TipoDocumento':
                            fattura.fiscal_document_type_id.id,
                        'dati_fattura_Data': fattura.date_invoice,
                        'dati_fattura_Numero': fattura.number,
                        'dati_fattura_iva_ids':
                            fattura._get_tax_comunicazione_dati_iva()
                    }
                    val = self._prepare_fattura_ricevuta(val, fattura)
                    vals_fatture.append((0, 0, val))

                val_cedente = {
                    'partner_id': cedente.id,
                    'fatture_ricevute_body_ids': vals_fatture
                }
                vals = self._prepare_cedente_partner_id(
                    cedente)
                val_cedente.update(vals)
                dati_fatture.append((0, 0, val_cedente))
            self.fatture_ricevute_ids = dati_fatture

    def _get_fatture_ricevute(self):
        invoices = False
        for comunicazione in self:
            domain = [('fiscal_document_type_id.type', 'in',
                       ['in_invoice', 'in_refund']),
                      ('company_id', '>=', comunicazione.company_id.id),
                      ('registration_date', '>=', comunicazione.date_start),
                      ('registration_date', '<=', comunicazione.date_end)]
            invoices = self.env['account.invoice'].search(domain)
        return invoices

    def _unlink_sections(self):
        for comunicazione in self:
            comunicazione.fatture_emesse_ids = False
            comunicazione.fatture_ricevute_ids = False

        return True

    def _validate(self):
        """
        Controllo congruità dati della comunicazione
        """
        return True

    def _export_xml_get_dati_fattura(self):
        # ----- 0 - Dati Fattura
        x_0_Dati_Fattura = etree.Element(
            etree.QName(NS_IV, "DatiFattura"), nsmap=NS_MAP)
        return x_0_Dati_Fattura

    def _export_xml_get_dati_fattura_header(self):
        # ----- 1 - Dati Fattura
        x_1_dati_fattura_header = etree.Element(
            etree.QName(NS_IV, "DatiFatturaHeader"), nsmap=NS_MAP)
        # ----- 1.1 - Progressivo Invio
        x_1_1_progressivo_invio = etree.SubElement(
            x_1_dati_fattura_header,
            etree.QName(NS_IV, "ProgressivoInvio"), nsmap=NS_MAP)
        x_1_1_progressivo_invio.text = str(self.identificativo)
        # ----- 1.2 - Dichiarante
        x_1_2_dichiarante = etree.SubElement(
            x_1_dati_fattura_header,
            etree.QName(NS_IV, "Dichiarante"), nsmap=NS_MAP)
        # ----- 1.2.1 - Codice Fiscale
        x_1_2_1_codice_fiscale = etree.SubElement(
            x_1_2_dichiarante,
            etree.QName(NS_IV, "CodiceFiscale"), nsmap=NS_MAP)
        # ----- 1.2.2 - Carica
        x_1_2_2_carica = etree.SubElement(
            x_1_2_dichiarante,
            etree.QName(NS_IV, "Carica"), nsmap=NS_MAP)
        return x_1_dati_fattura_header

    def _export_xml_get_dte(self):
        # ----- 2 - DTE
        x_2_dte = etree.Element(
            etree.QName(NS_IV, "DTE"), nsmap=NS_MAP)
        # -----     2.1 - Cedente Prestatore DTE
        x_2_1_cedente_prestatore = etree.SubElement(
            x_2_dte,
            etree.QName(NS_IV, "CedentePrestatoreDTE"), nsmap=NS_MAP)
        # -----         2.1.1 - IdentificativiFiscali
        x_2_1_1_identificativi_fiscali = etree.SubElement(
            x_2_1_cedente_prestatore,
            etree.QName(NS_IV, "IdentificativiFiscali"), nsmap=NS_MAP)
        # -----             2.1.1.1 - Id Fiscale IVA
        x_2_1_1_1_id_fiscale_iva = etree.SubElement(
            x_2_1_1_identificativi_fiscali,
            etree.QName(NS_IV, "IdFiscaleIVA"), nsmap=NS_MAP)
        # -----                 2.1.1.1.1 - Id Paese
        x_2_1_1_1_1_id_paese = etree.SubElement(
            x_2_1_1_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdPaese"), nsmap=NS_MAP)
        # -----                 2.1.1.1.2 - Id Codice
        x_2_1_1_1_2_id_codice = etree.SubElement(
            x_2_1_1_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdCodice"), nsmap=NS_MAP)
        # -----             2.1.1.2 - Codice Fiscale
        x_2_1_1_2_codice_fiscale = etree.SubElement(
            x_2_1_1_identificativi_fiscali,
            etree.QName(NS_IV, "CodiceFiscale"), nsmap=NS_MAP)
        # -----         2.1.2 - AltriDatiIdentificativi
        x_2_1_2_altri_identificativi = etree.SubElement(
            x_2_1_cedente_prestatore,
            etree.QName(NS_IV, "AltriDatiIdentificativi"), nsmap=NS_MAP)
        # -----             2.1.2.1 - Denominazione
        x_2_1_2_1_altri_identificativi = etree.SubElement(
            x_2_1_2_altri_identificativi,
            etree.QName(NS_IV, "Denominazione"), nsmap=NS_MAP)
        # -----             2.1.2.2 - Nome
        x_2_1_2_2_nome = etree.SubElement(
            x_2_1_2_altri_identificativi,
            etree.QName(NS_IV, "Nome"), nsmap=NS_MAP)
        # -----             2.1.2.3 - Cognome
        x_2_1_2_3_cognome = etree.SubElement(
            x_2_1_2_altri_identificativi,
            etree.QName(NS_IV, "Cognome"), nsmap=NS_MAP)
        # -----             2.1.2.4 - Sede
        x_2_1_2_4_sede = etree.SubElement(
            x_2_1_2_altri_identificativi,
            etree.QName(NS_IV, "Sede"), nsmap=NS_MAP)
        # -----                 2.1.2.4.1 - Indirizzo
        x_2_1_2_4_1_indirizzo = etree.SubElement(
            x_2_1_2_4_sede,
            etree.QName(NS_IV, "Indirizzo"), nsmap=NS_MAP)
        # -----                 2.1.2.4.2 - Numero Civico
        x_2_1_2_4_2_numero_civico = etree.SubElement(
            x_2_1_2_4_sede,
            etree.QName(NS_IV, "NumeroCivico"), nsmap=NS_MAP)
        # -----                 2.1.2.4.3 - CAP
        x_2_1_2_4_3_cap = etree.SubElement(
            x_2_1_2_4_sede,
            etree.QName(NS_IV, "CAP"), nsmap=NS_MAP)
        # -----                 2.1.2.4.4 - Comune
        x_2_1_2_4_4_comune = etree.SubElement(
            x_2_1_2_4_sede,
            etree.QName(NS_IV, "Comune"), nsmap=NS_MAP)
        # -----                 2.1.2.4.5 - Provincia
        x_2_1_2_4_5_comune = etree.SubElement(
            x_2_1_2_4_sede,
            etree.QName(NS_IV, "Provincia"), nsmap=NS_MAP)
        # -----                 2.1.2.4.6 - Nazione
        x_2_1_2_4_6_nazione = etree.SubElement(
            x_2_1_2_4_sede,
            etree.QName(NS_IV, "Nazione"), nsmap=NS_MAP)
        # -----             2.1.2.5 - Stabile Organizzazione
        x_2_1_2_5_stabile_organizzazione = etree.SubElement(
            x_2_1_2_altri_identificativi,
            etree.QName(NS_IV, "StabileOrganizzazione"), nsmap=NS_MAP)
        # -----                 2.1.2.5.1 - Indirizzo
        x_2_1_2_5_1_indirizzo = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Indirizzo"), nsmap=NS_MAP)
        # -----                 2.1.2.5.2 - Numero Civico
        x_2_1_2_5_2_numero_civico = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Numerocivico"), nsmap=NS_MAP)
        # -----                 2.1.2.5.3 - CAP
        x_2_1_2_5_3_cap = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "CAP"), nsmap=NS_MAP)
        # -----                 2.1.2.5.4 - Comune
        x_2_1_2_5_4_comune = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Comune"), nsmap=NS_MAP)
        # -----                 2.1.2.5.5 - Provincia
        x_2_1_2_5_5_provincia = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Provincia"), nsmap=NS_MAP)
        # -----                 2.1.2.5.6 - Nazione
        x_2_1_2_5_6_nazione = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Nazione"), nsmap=NS_MAP)
        # -----             2.1.2.6 - Rappresentante Fiscale
        x_2_1_2_6_rappresentante_fiscale = etree.SubElement(
            x_2_1_2_altri_identificativi,
            etree.QName(NS_IV, "RappresentanteFiscale"), nsmap=NS_MAP)
        # -----                 2.1.2.6.1 - Id Fiscale IVA
        x_2_1_2_6_1_id_fiscale_iva = etree.SubElement(
            x_2_1_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "IdFiscaleIVA"), nsmap=NS_MAP)
        # -----                     2.1.2.6.1.1 - Id Paese
        x_2_1_2_6_1_1_id_paese = etree.SubElement(
            x_2_1_2_6_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdPaese"), nsmap=NS_MAP)
        # -----                     2.1.2.6.1.2 - Id Codice
        x_2_1_2_6_1_2_id_codice = etree.SubElement(
            x_2_1_2_6_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdCodice"), nsmap=NS_MAP)
        # -----                 2.1.2.6.2 - Denominazione
        x_2_1_2_6_2_denominazione = etree.SubElement(
            x_2_1_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "Denominazione"), nsmap=NS_MAP)
        # -----                 2.1.2.6.3 - Nome
        x_2_1_2_6_3_nome = etree.SubElement(
            x_2_1_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "Nome"), nsmap=NS_MAP)
        # -----                 2.1.2.6.4 - Cognome
        x_2_1_2_6_4_cognome = etree.SubElement(
            x_2_1_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "Cognome"), nsmap=NS_MAP)
        invoices_grouped = self.group_invoices_for_partner(
            self.fatture_emesse_ids)
        for partner in invoices_grouped:
            first_invoice = invoices_grouped[partner][0]
            # -----     2.2 - Cessionario Committente DTE
            x_2_2_cessionario_committente = etree.SubElement(
                x_2_dte,
                etree.QName(NS_IV, "CessionarioCommittenteDTE"), nsmap=NS_MAP)
            # -----         2.2.1 - IdentificativiFiscali
            x_2_2_1_identificativi_fiscali = etree.SubElement(
                x_2_2_cessionario_committente,
                etree.QName(NS_IV, "IdentificativiFiscali"), nsmap=NS_MAP)
            # -----             2.2.1.1 - Id Fiscale IVA
            x_2_2_1_1_id_fiscale_iva = etree.SubElement(
                x_2_2_1_identificativi_fiscali,
                etree.QName(NS_IV, "IdFiscaleIVA"), nsmap=NS_MAP)
            # -----                 2.2.1.1.1 - Id Paese
            x_2_2_1_1_1_id_paese = etree.SubElement(
                x_2_2_1_1_id_fiscale_iva,
                etree.QName(NS_IV, "IdPaese"), nsmap=NS_MAP)
            x_2_2_1_1_1_id_paese.text = \
                first_invoice.cessionario_IdFiscaleIVA_IdPaese or ''
            # -----                 2.2.1.1.2 - Id Codice
            x_2_2_1_1_2_id_codice = etree.SubElement(
                x_2_2_1_1_id_fiscale_iva,
                etree.QName(NS_IV, "IdCodice"), nsmap=NS_MAP)
            x_2_2_1_1_2_id_codice.text = \
                first_invoice.cessionario_IdFiscaleIVA_IdCodice or ''
            # -----             2.2.1.2 - Codice Fiscale
            x_2_2_1_2_codice_fiscale = etree.SubElement(
                x_2_2_1_identificativi_fiscali,
                etree.QName(NS_IV, "CodiceFiscale"), nsmap=NS_MAP)
            x_2_2_1_2_codice_fiscale.text = \
                first_invoice.cessionario_CodiceFiscale or ''
            # -----         2.2.2 - AltriDatiIdentificativi
            x_2_2_2_altri_identificativi = etree.SubElement(
                x_2_2_cessionario_committente,
                etree.QName(NS_IV, "AltriDatiIdentificativi"), nsmap=NS_MAP)
            # -----             2.2.2.1 - Denominazione
            x_2_2_2_1_altri_identificativi_denominazione = etree.SubElement(
                x_2_2_2_altri_identificativi,
                etree.QName(NS_IV, "Denominazione"), nsmap=NS_MAP)
            x_2_2_2_1_altri_identificativi_denominazione.text = \
                first_invoice.cessionario_Denominazione or ''
            # -----             2.2.2.2 - Nome
            x_2_2_2_2_nome = etree.SubElement(
                x_2_2_2_altri_identificativi,
                etree.QName(NS_IV, "Nome"), nsmap=NS_MAP)
            x_2_2_2_2_nome.text = \
                first_invoice.cessionario_Nome or ''
            # -----             2.2.2.3 - Cognome
            x_2_2_2_3_cognome = etree.SubElement(
                x_2_2_2_altri_identificativi,
                etree.QName(NS_IV, "Cognome"), nsmap=NS_MAP)
            x_2_2_2_3_cognome.text = \
                first_invoice.cessionario_Cognome or ''
            # -----             2.2.2.4 - Sede
            x_2_2_2_4_sede = etree.SubElement(
                x_2_2_2_altri_identificativi,
                etree.QName(NS_IV, "Sede"), nsmap=NS_MAP)
            # -----                 2.2.2.4.1 - Indirizzo
            x_2_2_2_4_1_indirizzo = etree.SubElement(
                x_2_2_2_4_sede,
                etree.QName(NS_IV, "Indirizzo"), nsmap=NS_MAP)
            x_2_2_2_4_1_indirizzo.text = \
                first_invoice.cessionario_sede_Indirizzo or ''
            # -----                 2.2.2.4.2 - Numero Civico
            x_2_2_2_4_2_numero_civico = etree.SubElement(
                x_2_2_2_4_sede,
                etree.QName(NS_IV, "NumeroCivico"), nsmap=NS_MAP)
            x_2_2_2_4_2_numero_civico.text = \
                first_invoice.cessionario_sede_NumeroCivico or ''
            # -----                 2.2.2.4.3 - CAP
            x_2_2_2_4_3_cap = etree.SubElement(
                x_2_2_2_4_sede,
                etree.QName(NS_IV, "CAP"), nsmap=NS_MAP)
            x_2_2_2_4_3_cap.text = \
                first_invoice.cessionario_sede_Cap or ''
            # -----                 2.2.2.4.4 - Comune
            x_2_2_2_4_4_comune = etree.SubElement(
                x_2_2_2_4_sede,
                etree.QName(NS_IV, "Comune"), nsmap=NS_MAP)
            x_2_2_2_4_4_comune.text = \
                first_invoice.cessionario_sede_Comune or ''
            # -----                 2.2.2.4.5 - Provincia
            x_2_2_2_4_5_provincia = etree.SubElement(
                x_2_2_2_4_sede,
                etree.QName(NS_IV, "Provincia"), nsmap=NS_MAP)
            x_2_2_2_4_5_provincia.text = \
                first_invoice.cessionario_sede_Provincia or ''
            # -----                 2.2.2.4.6 - Nazione
            x_2_2_2_4_6_nazione = etree.SubElement(
                x_2_2_2_4_sede,
                etree.QName(NS_IV, "Nazione"), nsmap=NS_MAP)
            x_2_2_2_4_6_nazione.text = \
                first_invoice.cessionario_sede_Nazione or ''
            # -----             2.2.2.5 - Stabile Organizzazione
            x_2_2_2_5_stabile_organizzazione = etree.SubElement(
                x_2_2_2_altri_identificativi,
                etree.QName(NS_IV, "StabileOrganizzazione"), nsmap=NS_MAP)
            # -----                 2.2.2.5.1 - Indirizzo
            x_2_2_2_5_1_indirizzo = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione,
                etree.QName(NS_IV, "Indirizzo"), nsmap=NS_MAP)
            x_2_2_2_5_1_indirizzo.text = \
                first_invoice.cessionario_so_Indirizzo or ''
            # -----                 2.2.2.5.2 - Numero Civico
            x_2_2_2_5_2_numero_civico = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione,
                etree.QName(NS_IV, "NumeroCivico"), nsmap=NS_MAP)
            x_2_2_2_5_2_numero_civico.text = \
                first_invoice.cessionario_so_NumeroCivico or ''
            # -----                 2.2.2.5.3 - CAP
            x_2_2_2_5_3_cap = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione,
                etree.QName(NS_IV, "CAP"), nsmap=NS_MAP)
            x_2_2_2_5_3_cap.text = \
                first_invoice.cessionario_so_Cap or ''
            # -----                 2.2.2.5.4 - Comune
            x_2_2_2_5_4_comune = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione,
                etree.QName(NS_IV, "Comune"), nsmap=NS_MAP)
            x_2_2_2_5_4_comune.text = \
                first_invoice.cessionario_so_Comune or ''
            # -----                 2.2.2.5.5 - Provincia
            x_2_2_2_5_5_provincia = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione,
                etree.QName(NS_IV, "Provincia"), nsmap=NS_MAP)
            x_2_2_2_5_5_provincia.text = \
                first_invoice.cessionario_so_Provincia or ''
            # -----                 2.2.2.5.6 - Nazione
            x_2_2_2_5_6_nazione = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione,
                etree.QName(NS_IV, "Nazione"), nsmap=NS_MAP)
            x_2_2_2_5_6_nazione.text = \
                first_invoice.cessionario_so_Nazione or ''
            # -----             2.2.2.6 - Rappresentante Fiscale
            x_2_2_2_6_rappresentante_fiscale = etree.SubElement(
                x_2_2_2_altri_identificativi,
                etree.QName(NS_IV, "RappresentanteFiscale"), nsmap=NS_MAP)
            # -----                 2.2.2.6.1 - Id Fiscale IVA
            x_2_2_2_6_1_id_fiscale_iva = etree.SubElement(
                x_2_2_2_6_rappresentante_fiscale,
                etree.QName(NS_IV, "IdFiscaleIVA"), nsmap=NS_MAP)
            x_2_2_2_6_rappresentante_fiscale.text = \
                first_invoice.cessionario_rf_IdFiscaleIVA_IdPaese or ''
            # -----                     2.2.2.6.1.1 - Id Paese
            x_2_2_2_6_1_1_id_paese = etree.SubElement(
                x_2_2_2_6_1_id_fiscale_iva,
                etree.QName(NS_IV, "IdPaese"), nsmap=NS_MAP)
            x_2_2_2_6_1_1_id_paese.text = \
                first_invoice.cessionario_rf_IdFiscaleIVA_IdPaese or ''
            # -----                     2.2.2.6.1.2 - Id Codice
            x_2_2_2_6_1_2_id_codice = etree.SubElement(
                x_2_2_2_6_1_id_fiscale_iva,
                etree.QName(NS_IV, "IdCodice"), nsmap=NS_MAP)
            x_2_2_2_6_1_2_id_codice.text = \
                first_invoice.cessionario_rf_IdFiscaleIVA_IdCodice or ''
            # -----                 2.2.2.6.2 - Denominazione
            x_2_2_2_6_2_denominazione = etree.SubElement(
                x_2_2_2_6_rappresentante_fiscale,
                etree.QName(NS_IV, "Denominazione"), nsmap=NS_MAP)
            x_2_2_2_6_2_denominazione.text = \
                first_invoice.cessionario_rf_Denominazione or ''
            # -----                 2.2.2.6.3 - Nome
            x_2_2_2_6_3_nome = etree.SubElement(
                x_2_2_2_6_rappresentante_fiscale,
                etree.QName(NS_IV, "Nome"), nsmap=NS_MAP)
            x_2_2_2_6_3_nome.text = \
                first_invoice.cessionario_rf_Nome or ''
            # -----                 2.2.2.6.4 - Cognome
            x_2_2_2_6_4_cognome = etree.SubElement(
                x_2_2_2_6_rappresentante_fiscale,
                etree.QName(NS_IV, "Cognome"), nsmap=NS_MAP)
            x_2_2_2_6_4_cognome.text = \
                first_invoice.cessionario_rf_Cognome or ''
            for invoice in invoices_grouped[partner]:
                # -----         2.2.3 - Dati Fattura Body DTE
                x_2_2_3_dati_fattura_body_dte = etree.SubElement(
                    x_2_2_cessionario_committente,
                    etree.QName(NS_IV, "DatiFatturaBodyDTE"), nsmap=NS_MAP)
                # -----             2.2.3.1 - Dati Generali
                x_2_2_3_1_dati_generali = etree.SubElement(
                    x_2_2_3_dati_fattura_body_dte,
                    etree.QName(NS_IV, "DatiGenerali"), nsmap=NS_MAP)
                # -----                 2.2.3.1.1 - Tipo Documento
                x_2_2_3_1_1_tipo_documento = etree.SubElement(
                    x_2_2_3_1_dati_generali,
                    etree.QName(NS_IV, "TipoDocumento"), nsmap=NS_MAP)
                x_2_2_3_1_1_tipo_documento.text = \
                    invoice.dati_fattura_TipoDocumento.code
                # -----                 2.2.3.1.2 - Data
                x_2_2_3_1_2_data = etree.SubElement(
                    x_2_2_3_1_dati_generali,
                    etree.QName(NS_IV, "Data"), nsmap=NS_MAP)
                x_2_2_3_1_2_data.text = invoice.dati_fattura_Data
                # -----                 2.2.3.1.3 - Numero
                x_2_2_3_1_2_numero = etree.SubElement(
                    x_2_2_3_1_dati_generali,
                    etree.QName(NS_IV, "Numero"), nsmap=NS_MAP)
                x_2_2_3_1_2_numero.text = invoice.dati_fattura_Numero
                # -----             2.2.3.2 - Dati Riepilogo
                x_2_2_3_2_riepilogo = etree.SubElement(
                    x_2_2_3_dati_fattura_body_dte,
                    etree.QName(NS_IV, "DatiRiepilogo"), nsmap=NS_MAP)
                # -----                 2.2.3.2.1 - Imponibile Importo
                x_2_2_3_2_1_imponibile_importo = etree.SubElement(
                    x_2_2_3_2_riepilogo,
                    etree.QName(NS_IV, "ImponibileImporto"), nsmap=NS_MAP)
                # -----                 2.2.3.2.2 - Dati IVA
                x_2_2_3_2_2_dati_iva = etree.SubElement(
                    x_2_2_3_2_riepilogo,
                    etree.QName(NS_IV, "DatiIVA"), nsmap=NS_MAP)
                # -----                     2.2.3.2.2.1 - Imposta
                x_2_2_3_2_2_1_imposta = etree.SubElement(
                    x_2_2_3_2_2_dati_iva,
                    etree.QName(NS_IV, "Imposta"), nsmap=NS_MAP)
                # -----                     2.2.3.2.2.2 - Aliquota
                x_2_2_3_2_2_2_aliquota = etree.SubElement(
                    x_2_2_3_2_2_dati_iva,
                    etree.QName(NS_IV, "Aliquota"), nsmap=NS_MAP)
                # -----                 2.2.3.2.3 - Natura
                x_2_2_3_2_3_natura = etree.SubElement(
                    x_2_2_3_2_riepilogo,
                    etree.QName(NS_IV, "Natura"), nsmap=NS_MAP)
                # -----                 2.2.3.2.4 - Detraibile
                x_2_2_3_2_4_detraibile = etree.SubElement(
                    x_2_2_3_2_riepilogo,
                    etree.QName(NS_IV, "Detraibile"), nsmap=NS_MAP)
                # -----                 2.2.3.2.5 - Deducibile
                x_2_2_3_2_5_deducibile = etree.SubElement(
                    x_2_2_3_2_riepilogo,
                    etree.QName(NS_IV, "Deducibile"), nsmap=NS_MAP)
                # -----                 2.2.3.2.6 - Esigibilita IVA
                x_2_2_3_2_6_esagibilita_iva = etree.SubElement(
                    x_2_2_3_2_riepilogo,
                    etree.QName(NS_IV, "EsigibilitaIVA"), nsmap=NS_MAP)
        # -----     2.3 - Rettifica
        x_2_3_rettifica = etree.SubElement(
            x_2_dte,
            etree.QName(NS_IV, "Rettifica"), nsmap=NS_MAP)
        # -----         2.3.1 - Id File
        x_2_3_1_id_file = etree.SubElement(
            x_2_3_rettifica,
            etree.QName(NS_IV, "IdFile"), nsmap=NS_MAP)
        # x_2_3_1_id_file.text = self.rettifica_IdFIle \
        #     if self.rettifica_IdFIle else ''
        # -----         2.3.2 - Posizione
        x_2_3_2_posizione = etree.SubElement(
            x_2_3_rettifica,
            etree.QName(NS_IV, "Posizione"), nsmap=NS_MAP)
        # x_2_3_2_posizione.text = self.rettifica_Posizione \
        #     if self.rettifica_Posizione else ''
        return x_2_dte

    '''
    def _export_xml_get_dtr(self):
        # ----- 3 - DTR
        x_3_dtr = etree.Element(
            etree.QName(NS_IV, "DTR"), nsmap=NS_MAP)
        # -----     3.1 - Cedente Prestatore DTR
        x_3_1_cedente_prestatore = etree.SubElement(
            x_3_dtr,
            etree.QName(NS_IV, "CedentePrestatoreDTR"), nsmap=NS_MAP)
        # -----         3.1.1 - IdentificativiFiscali
        x_3_1_1_identificativi_fiscali = etree.SubElement(
            x_3_1_cedente_prestatore,
            etree.QName(NS_IV, "IdentificativiFiscali"), nsmap=NS_MAP)
        # -----             3.1.1.1 - Id Fiscale IVA
        x_3_1_1_1_id_fiscale_iva = etree.SubElement(
            x_3_1_1_identificativi_fiscali,
            etree.QName(NS_IV, "IdFiscaleIVA"), nsmap=NS_MAP)
        # -----                 3.1.1.1.1 - Id Paese
        x_3_1_1_1_1_id_paese = etree.SubElement(
            x_3_1_1_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdPaese"), nsmap=NS_MAP)
        # -----                 3.1.1.1.2 - Id Codice
        x_3_1_1_1_2_id_codice = etree.SubElement(
            x_3_1_1_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdCodice"), nsmap=NS_MAP)
        # -----             3.1.1.2 - Codice Fiscale
        x_3_1_1_2_codice_fiscale = etree.SubElement(
            x_3_1_1_identificativi_fiscali,
            etree.QName(NS_IV, "CodiceFiscale"), nsmap=NS_MAP)
        # -----         3.1.2 - AltriDatiIdentificativi
        x_3_1_2_altri_identificativi = etree.SubElement(
            x_3_1_cedente_prestatore,
            etree.QName(NS_IV, "AltriDatiIdentificativi"), nsmap=NS_MAP)
        # -----             3.1.2.1 - Denominazione
        x_3_1_2_1_altri_identificativi = etree.SubElement(
            x_3_1_2_altri_identificativi,
            etree.QName(NS_IV, "Denominazione"), nsmap=NS_MAP)
        # -----             3.1.2.2 - Nome
        x_3_1_2_2_nome = etree.SubElement(
            x_3_1_2_altri_identificativi,
            etree.QName(NS_IV, "Nome"), nsmap=NS_MAP)
        # -----             3.1.2.3 - Cognome
        x_3_1_2_3_cognome = etree.SubElement(
            x_3_1_2_altri_identificativi,
            etree.QName(NS_IV, "Cognome"), nsmap=NS_MAP)
        # -----             3.1.2.4 - Sede
        x_3_1_2_4_sede = etree.SubElement(
            x_3_1_2_altri_identificativi,
            etree.QName(NS_IV, "Sede"), nsmap=NS_MAP)
        # -----                 3.1.2.4.1 - Indirizzo
        x_3_1_2_4_1_indirizzo = etree.SubElement(
            x_3_1_2_4_sede,
            etree.QName(NS_IV, "Indirizzo"), nsmap=NS_MAP)
        # -----                 3.1.2.4.2 - Numero Civico
        x_3_1_2_4_2_numero_civico = etree.SubElement(
            x_3_1_2_4_sede,
            etree.QName(NS_IV, "NumeroCivico"), nsmap=NS_MAP)
        # -----                 3.1.2.4.3 - CAP
        x_3_1_2_4_3_cap = etree.SubElement(
            x_3_1_2_4_sede,
            etree.QName(NS_IV, "CAP"), nsmap=NS_MAP)
        # -----                 3.1.2.4.4 - Comune
        x_3_1_2_4_4_comune = etree.SubElement(
            x_3_1_2_4_sede,
            etree.QName(NS_IV, "Comune"), nsmap=NS_MAP)
        # -----                 3.1.2.4.5 - Provincia
        x_3_1_2_4_5_comune = etree.SubElement(
            x_3_1_2_4_sede,
            etree.QName(NS_IV, "Provincia"), nsmap=NS_MAP)
        # -----                 3.1.2.4.6 - Nazione
        x_3_1_2_4_6_nazione = etree.SubElement(
            x_3_1_2_4_sede,
            etree.QName(NS_IV, "Nazione"), nsmap=NS_MAP)
        # -----             3.1.2.5 - Stabile Organizzazione
        x_3_1_2_5_stabile_organizzazione = etree.SubElement(
            x_3_1_2_altri_identificativi,
            etree.QName(NS_IV, "StabileOrganizzazione"), nsmap=NS_MAP)
        # -----                 3.1.2.5.1 - Indirizzo
        x_3_1_2_5_1_indirizzo = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Indirizzo"), nsmap=NS_MAP)
        # -----                 3.1.2.5.2 - Numero Civico
        x_3_1_2_5_2_numero_civico = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Numerocivico"), nsmap=NS_MAP)
        # -----                 3.1.2.5.3 - CAP
        x_3_1_2_5_3_cap = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "CAP"), nsmap=NS_MAP)
        # -----                 3.1.2.5.4 - Comune
        x_3_1_2_5_4_comune = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Comune"), nsmap=NS_MAP)
        # -----                 3.1.2.5.5 - Provincia
        x_3_1_2_5_5_provincia = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Provincia"), nsmap=NS_MAP)
        # -----                 3.1.2.5.6 - Nazione
        x_3_1_2_5_6_nazione = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Nazione"), nsmap=NS_MAP)
        # -----             3.1.2.6 - Rappresentante Fiscale
        x_3_1_2_6_rappresentante_fiscale = etree.SubElement(
            x_3_1_2_altri_identificativi,
            etree.QName(NS_IV, "RappresentanteFiscale"), nsmap=NS_MAP)
        # -----                 3.1.2.6.1 - Id Fiscale IVA
        x_3_1_2_6_1_id_fiscale_iva = etree.SubElement(
            x_3_1_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "IdFiscaleIVA"), nsmap=NS_MAP)
        # -----                     3.1.2.6.1.1 - Id Paese
        x_3_1_2_6_1_1_id_paese = etree.SubElement(
            x_3_1_2_6_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdPaese"), nsmap=NS_MAP)
        # -----                     3.1.2.6.1.2 - Id Codice
        x_3_1_2_6_1_2_id_codice = etree.SubElement(
            x_3_1_2_6_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdCodice"), nsmap=NS_MAP)
        # -----                 3.1.2.6.2 - Denominazione
        x_3_1_2_6_2_denominazione = etree.SubElement(
            x_3_1_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "Denominazione"), nsmap=NS_MAP)
        # -----                 3.1.2.6.3 - Nome
        x_3_1_2_6_3_nome = etree.SubElement(
            x_3_1_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "Nome"), nsmap=NS_MAP)
        # -----                 3.1.2.6.4 - Cognome
        x_3_1_2_6_4_cognome = etree.SubElement(
            x_3_1_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "Cognome"), nsmap=NS_MAP)
        # -----     3.2 - Cessionario Committente DTR
        x_3_2_cessionario_committente = etree.SubElement(
            x_3_dtr,
            etree.QName(NS_IV, "CessionarioCommittenteDTR"), nsmap=NS_MAP)
        # -----         3.2.1 - IdentificativiFiscali
        x_3_2_1_identificativi_fiscali = etree.SubElement(
            x_3_2_cessionario_committente,
            etree.QName(NS_IV, "IdentificativiFiscali"), nsmap=NS_MAP)
        # -----             3.2.1.1 - Id Fiscale IVA
        x_3_2_1_1_id_fiscale_iva = etree.SubElement(
            x_3_2_1_identificativi_fiscali,
            etree.QName(NS_IV, "IdFiscaleIVA"), nsmap=NS_MAP)
        # -----                 3.2.1.1.1 - Id Paese
        x_3_2_1_1_1_id_paese = etree.SubElement(
            x_3_2_1_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdPaese"), nsmap=NS_MAP)
        # -----                 3.2.1.1.2 - Id Paese
        x_3_2_1_1_2_id_codice = etree.SubElement(
            x_3_2_1_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdCodice"), nsmap=NS_MAP)
        # -----             3.2.1.2 - Codice Fiscale
        x_3_2_1_2_codice_fiscale = etree.SubElement(
            x_3_2_1_identificativi_fiscali,
            etree.QName(NS_IV, "CodiceFiscale"), nsmap=NS_MAP)
        # -----         3.2.2 - AltriDatiIdentificativi
        x_3_2_2_altri_identificativi = etree.SubElement(
            x_3_2_cessionario_committente,
            etree.QName(NS_IV, "AltriDatiIdentificativi"), nsmap=NS_MAP)
        # -----             3.2.2.1 - Denominazione
        x_3_2_2_1_altri_identificativi = etree.SubElement(
            x_3_2_2_altri_identificativi,
            etree.QName(NS_IV, "Denominazione"), nsmap=NS_MAP)
        # -----             3.2.2.2 - Nome
        x_3_2_2_2_nome = etree.SubElement(
            x_3_2_2_altri_identificativi,
            etree.QName(NS_IV, "Nome"), nsmap=NS_MAP)
        # -----             3.2.2.3 - Cognome
        x_3_2_2_3_cognome = etree.SubElement(
            x_3_2_2_altri_identificativi,
            etree.QName(NS_IV, "Cognome"), nsmap=NS_MAP)
        # -----             3.2.2.4 - Sede
        x_3_2_2_4_sede = etree.SubElement(
            x_3_2_2_altri_identificativi,
            etree.QName(NS_IV, "Sede"), nsmap=NS_MAP)
        # -----                 3.2.2.4.1 - Indirizzo
        x_3_2_2_4_1_indirizzo = etree.SubElement(
            x_3_2_2_4_sede,
            etree.QName(NS_IV, "Indirizzo"), nsmap=NS_MAP)
        # -----                 3.2.2.4.2 - Numero Civico
        x_3_2_2_4_2_numero_civico = etree.SubElement(
            x_3_2_2_4_sede,
            etree.QName(NS_IV, "NumeroCivico"), nsmap=NS_MAP)
        # -----                 3.2.2.4.3 - CAP
        x_3_2_2_4_3_cap = etree.SubElement(
            x_3_2_2_4_sede,
            etree.QName(NS_IV, "CAP"), nsmap=NS_MAP)
        # -----                 3.2.2.4.4 - Comune
        x_3_2_2_4_4_comune = etree.SubElement(
            x_3_2_2_4_sede,
            etree.QName(NS_IV, "Comune"), nsmap=NS_MAP)
        # -----                 3.2.2.4.5 - Provincia
        x_3_2_2_4_5_comune = etree.SubElement(
            x_3_2_2_4_sede,
            etree.QName(NS_IV, "Provincia"), nsmap=NS_MAP)
        # -----                 3.2.2.4.6 - Nazione
        x_3_2_2_4_6_nazione = etree.SubElement(
            x_3_2_2_4_sede,
            etree.QName(NS_IV, "Nazione"), nsmap=NS_MAP)
        # -----             3.2.2.5 - Stabile Organizzazione
        x_3_2_2_5_stabile_organizzazione = etree.SubElement(
            x_3_2_2_altri_identificativi,
            etree.QName(NS_IV, "StabileOrganizzazione"), nsmap=NS_MAP)
        # -----                 3.2.2.5.1 - Indirizzo
        x_3_2_2_5_1_indirizzo = etree.SubElement(
            x_3_2_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Indirizzo"), nsmap=NS_MAP)
        # -----                 3.2.2.5.2 - Numero Civico
        x_3_2_2_5_2_numero_civico = etree.SubElement(
            x_3_2_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "NumeroCivico"), nsmap=NS_MAP)
        # -----                 3.2.2.5.3 - CAP
        x_3_2_2_5_3_cap = etree.SubElement(
            x_3_2_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "CAP"), nsmap=NS_MAP)
        # -----                 3.2.2.5.4 - Comune
        x_3_2_2_5_4_comune = etree.SubElement(
            x_3_2_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Comune"), nsmap=NS_MAP)
        # -----                 3.2.2.5.5 - Provincia
        x_3_2_2_5_5_provincia = etree.SubElement(
            x_3_2_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Provincia"), nsmap=NS_MAP)
        # -----                 3.2.2.5.6 - Nazione
        x_3_2_2_5_6_nazione = etree.SubElement(
            x_3_2_2_5_stabile_organizzazione,
            etree.QName(NS_IV, "Nazione"), nsmap=NS_MAP)
        # -----             3.2.2.6 - Rappresentante Fiscale
        x_3_2_2_6_rappresentante_fiscale = etree.SubElement(
            x_3_2_2_altri_identificativi,
            etree.QName(NS_IV, "RappresentanteFiscale"), nsmap=NS_MAP)
        # -----                 3.2.2.6.1 - Id Fiscale IVA
        x_3_2_2_6_1_id_fiscale_iva = etree.SubElement(
            x_3_2_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "IdFiscaleIVA"), nsmap=NS_MAP)
        # -----                     3.2.2.6.1.1 - Id Paese
        x_3_2_2_6_1_1_id_paese = etree.SubElement(
            x_3_2_2_6_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdPaese"), nsmap=NS_MAP)
        # -----                     3.2.2.6.1.2 - Id Codice
        x_3_2_2_6_1_2_id_codice = etree.SubElement(
            x_3_2_2_6_1_id_fiscale_iva,
            etree.QName(NS_IV, "IdCodice"), nsmap=NS_MAP)
        # -----                 3.2.2.6.2 - Denominazione
        x_3_2_2_6_2_denominazione = etree.SubElement(
            x_3_2_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "Denominazione"), nsmap=NS_MAP)
        # -----                 3.2.2.6.3 - Nome
        x_3_2_2_6_3_nome = etree.SubElement(
            x_3_2_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "Nome"), nsmap=NS_MAP)
        # -----                 3.2.2.6.4 - Cognome
        x_3_2_2_6_4_cognome = etree.SubElement(
            x_3_2_2_6_rappresentante_fiscale,
            etree.QName(NS_IV, "Cognome"), nsmap=NS_MAP)
        # -----         3.2.3 - Dati Fattura Body DTR
        x_3_2_3_dati_fattura_body_dtr = etree.SubElement(
            x_3_2_cessionario_committente,
            etree.QName(NS_IV, "DatiFatturaBodyDTR"), nsmap=NS_MAP)
        # -----             3.2.3.1 - Dati Generali
        x_3_2_3_1_dati_generali = etree.SubElement(
            x_3_2_3_dati_fattura_body_dtr,
            etree.QName(NS_IV, "DatiGenerali"), nsmap=NS_MAP)
        # -----                 3.2.3.1.1 - Tipo Documento
        x_3_2_3_1_1_tipo_documento = etree.SubElement(
            x_3_2_3_1_dati_generali,
            etree.QName(NS_IV, "TipoDocumento"), nsmap=NS_MAP)
        # -----                 3.2.3.1.2 - Data
        x_3_2_3_1_2_data = etree.SubElement(
            x_3_2_3_1_dati_generali,
            etree.QName(NS_IV, "Data"), nsmap=NS_MAP)
        # -----                 3.2.3.1.3 - Numero
        x_3_2_3_1_2_numero = etree.SubElement(
            x_3_2_3_1_dati_generali,
            etree.QName(NS_IV, "Numero"), nsmap=NS_MAP)
        # -----             3.2.3.2 - Dati Riepilogo
        x_3_2_3_2_riepilogo = etree.SubElement(
            x_3_2_3_dati_fattura_body_dtr,
            etree.QName(NS_IV, "DatiRiepilogo"), nsmap=NS_MAP)
        # -----                 3.2.3.2.1 - Imponibile Importo
        x_3_2_3_2_1_imponibile_importo = etree.SubElement(
            x_3_2_3_2_riepilogo,
            etree.QName(NS_IV, "ImponibileImporto"), nsmap=NS_MAP)
        # -----                 3.2.3.2.2 - Dati IVA
        x_3_2_3_2_2_dati_iva = etree.SubElement(
            x_3_2_3_2_riepilogo,
            etree.QName(NS_IV, "DatiIVA"), nsmap=NS_MAP)
        # -----                     3.2.3.2.2.1 - Imposta
        x_3_2_3_2_2_1_imposta = etree.SubElement(
            x_3_2_3_2_2_dati_iva,
            etree.QName(NS_IV, "Imposta"), nsmap=NS_MAP)
        # -----                     3.2.3.2.2.2 - Aliquota
        x_3_2_3_2_2_2_aliquota = etree.SubElement(
            x_3_2_3_2_2_dati_iva,
            etree.QName(NS_IV, "Aliquota"), nsmap=NS_MAP)
        # -----                 3.2.3.2.3 - Natura
        x_3_2_3_2_3_natura = etree.SubElement(
            x_3_2_3_2_riepilogo,
            etree.QName(NS_IV, "Natura"), nsmap=NS_MAP)
        # -----                 3.2.3.2.4 - Detraibile
        x_3_2_3_2_4_detraibile = etree.SubElement(
            x_3_2_3_2_riepilogo,
            etree.QName(NS_IV, "Detraibile"), nsmap=NS_MAP)
        # -----                 3.2.3.2.5 - Deducibile
        x_3_2_3_2_5_deducibile = etree.SubElement(
            x_3_2_3_2_riepilogo,
            etree.QName(NS_IV, "Deducibile"), nsmap=NS_MAP)
        # -----                 3.2.3.2.6 - Esigibilita IVA
        x_3_2_3_2_6_esagibilita_iva = etree.SubElement(
            x_3_2_3_2_riepilogo,
            etree.QName(NS_IV, "EsigibilitaIVA"), nsmap=NS_MAP)
        # -----     3.3 - Rettifica
        x_3_3_rettifica = etree.SubElement(
            x_3_dtr,
            etree.QName(NS_IV, "Rettifica"), nsmap=NS_MAP)
        # -----         3.3.1 - Id File
        x_3_3_1_id_file = etree.SubElement(
            x_3_3_rettifica,
            etree.QName(NS_IV, "IdFile"), nsmap=NS_MAP)
        # -----         3.3.2 - Posizione
        x_3_3_2_posizione = etree.SubElement(
            x_3_3_rettifica,
            etree.QName(NS_IV, "Posizione"), nsmap=NS_MAP)
        return x_3_dtr
    '''

    def _export_xml_get_ann(self):
        # ----- 4 - ANN
        x_4_ann = etree.Element(
            etree.QName(NS_IV, "ANN"), nsmap=NS_MAP)
        # ----- 4.1 - Id File
        x_4_1_id_file = etree.SubElement(
            x_4_ann,
            etree.QName(NS_IV, "IdFile"), nsmap=NS_MAP)
        # ----- 4.2 - Posizione
        x_4_2_posizione = etree.SubElement(
            x_4_ann,
            etree.QName(NS_IV, "Posizione"), nsmap=NS_MAP)
        return x_4_ann

    def get_export_xml(self):
        self._validate()
        # ----- 0 - Dati Fattura
        x_0_dati_fattura = self._export_xml_get_dati_fattura()
        # ----- 1 - Dati Fattura header
        x_1_dati_fattura_header = self._export_xml_get_dati_fattura_header()
        x_0_dati_fattura.append(x_1_dati_fattura_header)
        # ----- 2 - DTE
        x_2_dte = self._export_xml_get_dte()
        x_0_dati_fattura.append(x_2_dte)
        # ----- 3 - DTR
        # x_3_dtr = self._export_xml_get_dtr()
        # x_0_dati_fattura.append(x_3_dtr)
        # ----- 4 - ANN
        # x_4_ann = self._export_xml_get_ann()
        # x_0_dati_fattura.append(x_4_ann)
        # ----- Create XML
        xml_string = etree.tostring(
            x_0_dati_fattura, encoding='utf8', method='xml', pretty_print=True)
        print '----------------------------------------'
        print xml_string
        print '----------------------------------------'
        return xml_string


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
        "Posizione", help="della fattura all'interno del file trasmesso",
        required=True)
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
        "Posizione", help="della fattura all'interno del file trasmesso",
        required=True)
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
