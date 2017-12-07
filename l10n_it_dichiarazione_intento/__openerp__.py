# -*- coding: utf-8 -*-
# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Dichiarazione Intento',
    'description': """
        Manage italian dichiarazione di intento""",
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Francesco Apruzzese',
    'website': 'http://www.apuliasoftware.it',
    'depends': [
        'account',
        'sale',
        'l10n_it',
        ],
    'data': [
        'views/sale_view.xml',
        'views/account_view.xml',
        'views/dichiarazione_intento_view.xml',
        'views/account_invoice_view.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
    'auto_install': False,
}
