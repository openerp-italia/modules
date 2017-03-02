# -*- encoding: utf-8 -*-
##########################################################################
#    Autor: Alessandro Camilli (a.camilli@yahoo.it)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
{
    "name": "Partners dichiarazioni intento",
    "version": "1.0",
    'author': 'Alessandro Camilli - Openforce',
    'website': 'http://www.openforce.it',
    "category": "Partners Modules",
    'description': """
        It handle fields of 'dichiarazione intento' to be printed on invoice
    """,
    "depends": ["account"],
    "init_xml": [],
    "demo_xml": [],
    "data": [
        "dichiarazione_sequence.xml",
        "partner/partner_view.xml",
        "views/report_invoice.xml"
    ],
    "installable": True,
    "active": True
}
