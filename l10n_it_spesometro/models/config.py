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


from openerp import models, fields, api, _


class res_country(models.Model):
    _inherit = "res.country"
    
    codice_stato_agenzia_entrate = fields.Char( 
        string = 'Codice stato Agenzia Entrate', size=3)
    
    
class res_partner(models.Model):
    _inherit = "res.partner"
    
    spesometro_escludi = fields.Boolean('Escludi', default=False)
    spesometro_operazione = fields.Selection(
        (('FA','Operazioni documentate da fattura'), 
        ('SA','Operazioni senza fattura'),
        ('BL1','Operazioni con paesi con fiscalità privilegiata'),
        ('BL2','Operazioni con soggetti non residenti'),
        ('BL3','Acquisti di servizi da soggetti non residenti'),
        ('DR','Documento Riepilogativo')),
        'Operazione' )
    
    spesometro_operazione_tipo_importo = fields.Selection((
                                ('INE','Imponibile, Non Imponibile, Esente'), 
                                ('NS','Non Soggette ad IVA'),
                                ('NV','Note di variazione')),
                   'Tipo Importo' )
    spesometro_IVA_non_esposta = fields.Boolean('IVA non esposta')
    spesometro_leasing = fields.Selection((('A','Autovettura'), 
                                           ('B','Caravan'),
                                           ('C','Altri veicoli'),
                                           ('D','Unità da diporto'),
                                           ('E','Aeromobili')),
                                          'Tipo Leasing')
    spesometro_tipo_servizio = fields.Selection(
        (('cessione','Cessione Beni'), 
        ('servizi','Prestazione di servizi')),
        'Tipo servizio', 
        help="Specificare per 'Operazioni con soggetti non residenti' ")
    
