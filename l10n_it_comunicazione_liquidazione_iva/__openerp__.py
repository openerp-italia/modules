# -*- coding: utf-8 -*-
# © 2017 Alessandro Camilli - Openforce
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

{
    'name': 'Comunicazione liquidazione IVA',
    'description': 'Gestione Comunicazione liquidazione IVA ed export file '
                   'xml conforme alle specifiche dell''Agenzia delle Entrate',
    'version': '8.0.1.0.0',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro",
    'website': 'http://www.odoo-italia.net',
    'license': 'GPL-3',
    'depends': [
        'account', 'l10n_it_codici_carica', 'l10n_it_fiscalcode'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/comunicazione_liquidazione.xml',
        'wizard/export_file_view.xml',
        'security/security.xml',
    ],
    'installable': True,
}
