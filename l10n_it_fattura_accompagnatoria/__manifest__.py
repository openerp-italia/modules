# -*- coding: utf-8 -*-
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Fattura Accompagnatoria",
    'summary': 'Stampa della fattura accompagnatoria',
    "version": "10.0.0.1.1",
    "category": "Accounting",
    "website": "https://www.agilebg.com/",
    "author": "Agile Business Group",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_ddt",
    ],
    "data": [
        "views/report_invoice.xml",
    ],
}
