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

{
    'name': 'Spesometro - Comunicazione art.21',
    'version': '0.1',
    'category': 'Account',
    'description': """
Functionalities:
- Creazione comunicazione art.21 in forma Aggregata
- Export file per agenzia delle entrate
    """,
    'author': 'Openforce di Alessandro Camilli',
    'website': 'http://www.openforce.it/',
    'license': 'AGPL-3',
    "depends": [
        'account', 'l10n_it_fiscalcode'
        ],
    "data": [
        'security/ir.model.access.csv',
        'wizard/export_file_view.xml',
        'views/account.xml',
        'views/config.xml',
        'views/spesometro.xml',
        ],
    "demo": [],
    "active": False,
    "installable": False
}

