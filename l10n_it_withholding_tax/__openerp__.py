# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2015 Alessandro Camilli 
#    (<http://www.openforce.it>)
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
{
    'name': 'Withholding tax',
    'version': '0.2',
    'category': 'Account',
    'description': """
    Withholding tax

""",
    'author': 'Openforce di Alessandro Camilli',
    'website': 'http://www.openforce.it',
    'license': 'AGPL-3',
    "depends" : ['account', 'account_voucher'],
    "data" : [
        'views/account.xml',
        'views/voucher.xml',
        'views/withholding_tax.xml',
        'wizard/create_wt_statement_view.xml',
        'security/ir.model.access.csv',
        'workflow.xml',
        ],
    "demo" : [],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: