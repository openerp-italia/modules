# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Alessandro Camilli (a.camilli@openforce.it)
#    Copyright (C) 2015
#    Openforce di Camilli Alessandro - www.openforce.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import models, fields, api


class account_tax_code(models.Model):
    _inherit = "account.tax.code"
    spesometro_escludi = fields.Boolean(string='Escludi dalla dichiarazione',
                                        default=False)


class account_journal(models.Model):
    _inherit = "account.journal"

    spesometro = fields.Boolean('Da includere')
    spesometro_operazione = fields.Selection((
        ('FA', 'FA - Operazioni documentate da fattura'),
        ('SA', 'SA - Operazioni senza fattura'),
        ('BL1', 'BL1 - Operazioni con paesi con fiscalità privilegiata'),
        ('BL2', 'BL2 - Operazioni con soggetti non residenti'),
        ('BL3', 'BL3 - Acquisti di servizi da soggetti non residenti'),
        ('DR', 'DR - Documento Riepilogativo')),
        'Operazione')
    spesometro_segno = fields.Selection((
        ('attiva', 'Attiva'),
        ('passiva', 'Passiva')),
        'Segno operaz.')
    spesometro_IVA_non_esposta = fields.Boolean('IVA non esposta')
    spesometro_operazione_tipo_importo = fields.Selection((
        ('INE', 'Imponibile, Non Imponibile, Esente'),
        ('NS', 'Non Soggette ad IVA'),
        ('NV', 'Note di variazione')),
        'Tipo Importo')
