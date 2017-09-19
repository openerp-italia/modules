# -*- coding: utf-8 -*-

import base64
from openerp import api, fields, models, exceptions


class ComunicazioneDatiIvaRicalcoloTipoDocumentoFiscale(models.TransientModel):
    _name = "comunicazione.dati.iva.ricalcolo.tipo.document.fiscale"
    _description = "Ricalcolo tipo documento fiscale su fatture"

    @api.multi
    def compute(self):
        comunicazione_ids = self._context.get('active_ids')
        for wizard in self:
            for comunicazione in self.env['comunicazione.dati.iva'].\
                    browse(comunicazione_ids):
                fatture_emesse = comunicazione._get_fatture_emesse()
                fatture_ricevute = comunicazione._get_fatture_ricevute()
                fatture = fatture_emesse + fatture_ricevute
                for fattura in fatture:
                    fattura.fiscal_document_type_id =\
                        fattura._get_document_fiscal_type(
                            type=fattura.type, partner=fattura.partner_id,
                            fiscal_position=fattura.fiscal_position,
                            journal=fattura.journal_id)[0] or False
            return {}
