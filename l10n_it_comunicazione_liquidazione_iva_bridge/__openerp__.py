# -*- coding: utf-8 -*-
# © 2017 Alessandro Camilli - Openforce
#
# This software and associated files (the "Software") may only be used
# (executed, modified, executed after modifications) if you have purchased a
# valid license from the authors, typically via Odoo Apps, or if you have
# received a written agreement from the authors of the Software
#
# You may develop Odoo modules that use the Software as a library (typically by
# depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the
# Software or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

{
    'name': 'Comunicazione liquidazione IVA Bridge',
    'summary': 'Bridge per importare i dati della liquidazione iva nella'
    'comunicazione liquidazione IVA',
    'version': '8.0.1.0.0',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro",
    'website': 'http://odoo-italia.net',
    'license': 'LGPL-3',
    'depends': [
        'account_vat_period_end_statement',
        'l10n_it_comunicazione_liquidazione_iva'
    ],
    'data': [
        'views/comunicazione_liquidazione.xml',
    ],
    'installable': True,
}
