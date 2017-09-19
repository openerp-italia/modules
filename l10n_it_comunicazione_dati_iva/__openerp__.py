# -*- coding: utf-8 -*-
# © 2017 Alessandro Camilli - Openforce
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

{
    'name': 'Comunicazione dati IVA',
    'description': 'Gestione Comunicazione dati IVA ed export file '
                   'xml conforme alle specifiche dell''Agenzia delle Entrate',
    'version': '8.0.1.0.0',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro",
    'website': 'http://www.odoo-italia.net',
    'license': 'GPL-3',
    'depends': [
        'account', 'l10n_it_fiscal_document_type', 'l10n_it_codici_carica',
        'l10n_it_fiscalcode', 'l10n_it_esigibilita_iva',
        'l10n_it_account_tax_kind', 'account_invoice_entry_date'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/compute_fiscal_document_type_view.xml',
        'views/comunicazione.xml',
        'wizard/export_file_view.xml',
    ],
    'installable': True,
}
