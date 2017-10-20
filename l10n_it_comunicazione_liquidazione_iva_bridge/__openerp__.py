# -*- coding: utf-8 -*-
# © 2017 Alessandro Camilli - Openforce
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

{
    'name': 'Comunicazione liquidazione IVA Bridge',
    'description': 'Bridge per importare i dati della liquidazione iva nella'
                   ' comunicazione liquidazione IVA',
    'version': '8.0.1.0.0',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro",
    'website': 'http://www.odoo-italia.net',
    'license': 'GPL-3',
    'depends': [
        'account_vat_period_end_statement',
        'l10n_it_comunicazione_liquidazione_iva',
        'l10n_it_esigibilita_iva',
    ],
    'data': [
        'views/comunicazione_liquidazione.xml',
    ],
    'installable': True,
}
