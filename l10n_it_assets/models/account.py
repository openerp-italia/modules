# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract (http://www.abstract.it)
#                       Openforce di Camilli Alessandro - www.openforce.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import models, fields, api


class account_move(models.Model):
    _inherit = 'account.move'
    
    asset_remove_move_id = fields.Many2one('account.move', 
                                           string='Move of Asset remove', 
                                           ondelete='set null')
    
    def _get_fields_affects_asset_move(self):
        '''
        List of move's fields that can't be modified if move is linked
        with a depreciation line
        '''
        res = ['period_id', 'journal_id', 'date']
        res =[] # <<<< test
        return res
    
    def _asset_control_on_write(self, cr, uid, ids, vals, context=None):
        return True
                    

class account_move_line(models.Model):
    _inherit = 'account.move.line'
    
    def _get_fields_affects_asset_move_line(self):
        '''
        List of move line's fields that can't be modified if move is linked
        with a depreciation line
        '''
        res = ['credit', 'debit', 'account_id', 'journal_id', 'date',
         'asset_category_id', 'asset_id', 'tax_code_id', 'tax_amount']
        res =[] # <<<< test
        return res
    
    def _asset_control_on_write(self, cr, uid, ids, vals, context=None, 
                                check=True, update_check=True):
        # Omitted standard controls
        return True
    
    def _asset_control_on_create(self, cr, uid, vals, context=None, check=True):
        # Omitted standard controls
        return True
    
    def create(self, cr, uid, vals, context=None, check=True):
        if not context:
            context = {}
        context.update({'allow_asset': True})
        return super(account_move_line, self).create(
            cr, uid, vals, context, check)
        
        
class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'
    
    date_invoice = fields.Date(string='Date Invoice',
                               store=True,
                               related='invoice_id.date_invoice')
    
    def move_line_get_item(self, cr, uid, line, context=None):
        res = super(account_invoice_line, self).move_line_get_item(
            cr, uid, line, context)
        if line.asset_id:
            res['asset_id'] = line.asset_id.id
        return res
    
    
class account_invoice(models.Model):
    _inherit = "account.invoice"
    
    @api.model
    def line_get_convert(self, line, part, date):
        res = super(account_invoice, self).line_get_convert(line, part, date)
        if 'asset_id' in line:
            res.update({'asset_id':line['asset_id']})
        return res
    
