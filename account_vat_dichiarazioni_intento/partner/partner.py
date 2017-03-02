# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp.osv import osv, fields, orm
from datetime import date


class res_partner(orm.Model):
    
    def get_sequence_registration_number(self, cr, uid, ids, context=None):
        
        res = {}
        today = date.today()
        
        self.write(cr, uid, ids, {
            'dichiarazione_intento_registration_number': self.pool.get('ir.sequence').get(cr, uid, 'partner.dichiarazioni.intento'),
            'dichiarazione_intento_registration_date': today,
            }, context=context)
        
        return res
        
    _inherit = 'res.partner'
    
    _columns = {
        'dichiarazione_intento_partner_number':  fields.char('Dichiarazione numero', size=64),
        'dichiarazione_intento_partner_date':  fields.date('Dichiarazione data'),
        'dichiarazione_intento_registration_number':  fields.char('Registrazione numero', size=64),
        'dichiarazione_intento_registration_date':  fields.date('Registrazione data'),
    }

    _defaults = {
    }
    
    #-----------------------------------------------------------------------------
    # EVITARE LA COPIA DI 'NUMERO della registrazione di intento'
    #-----------------------------------------------------------------------------
    def copy(self, cr, uid, id, default={}, context=None):
        default.update({'dichiarazione_intento_registration_number': '',
                        'dichiarazione_intento_registration_date': 0,
                        })
        return super(res_partner, self).copy(cr, uid, id, default, context)
    
    