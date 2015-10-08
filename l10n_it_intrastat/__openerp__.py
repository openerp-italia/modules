# -*- coding: utf-8 -*-
##############################################################################
#    
#    Author: Alessandro Camilli (a.camilli@openforce.it)
#    Copyright (C) 2015
#    Apulia Software srl - info@apuliasoftware.it - www.apuliasoftware.it
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

{
    'name': 'Account - Intrastat',
    'version': '0.1',
    'category': 'Account',
    'description': """
    Taxation and customs European Union statements.
    """,
    'author': 'Openforce di Alessandro Camilli per Apulia Software srl',
    'website': 'http://apuliasoftware.it/',
    'license': 'AGPL-3',
    "depends": [
        'account',
        'product',
        'stock',
        'stock_account',
        'report_intrastat'],
    "data": [
        'security/ir.model.access.csv',
        'views/intrastat.xml',
        'views/product.xml',
        'views/account.xml',
        'views/config.xml',
        ],
    "demo": [
        'demo/product_demo.xml'     
        ],
    "active": False,
    "installable": True
}

