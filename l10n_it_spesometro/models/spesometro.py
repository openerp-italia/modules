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


from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm, ValidationError
from datetime import datetime, date


class spesometro_configurazione(models.Model):

    @api.one
    @api.constrains('anno')
    def _check_one_year(self):
        domain = [('anno', '=', self.anno)]
        element_ids = self.search(domain)
        if len(element_ids) > 1:
            raise ValidationError(
                _('Error! Config for this year already exists'))

    _name = "spesometro.configurazione"
    _description = "Spesometro - Configurazione"

    anno = fields.Integer(string='Anno', size=4, required=True)
    stato_san_marino = fields.Many2one('res.country', string='Stato San Marino',
                                       required=True)
    regole_ids = fields.One2many('spesometro.regole', 'configurazione_id',
                                 string='Regole')
    quadro_fa_limite_importo = \
        fields.Float(string='Quadro FA - Limite importo')
    quadro_fa_limite_importo_line = \
        fields.Float(string='Quadro FA - Limite importo singola operaz.')
    quadro_sa_limite_importo = \
        fields.Float(string='Quadro SA - Limite importo')
    quadro_sa_limite_importo_line = \
        fields.Float(string='Quadro SA - Limite importo singola operaz.')
    quadro_bl1_limite_importo = \
        fields.Float(string='Quadro BL - Operazioni con paesi con fiscalità \
                    privilegiata - Limite importo')
    quadro_bl1_limite_importo_line = \
        fields.Float(string='Quadro BL - Operazioni con paesi con fiscalità \
                    privilegiata - Limite importo singola operaz.')
    quadro_bl2_limite_importo = \
        fields.Float(string='Quadro BL - Operazioni con soggetti non \
                    residenti - Limite importo')
    quadro_bl2_limite_importo_line = \
        fields.Float(string='Quadro BL - Operazioni con soggetti non \
                    residenti - Limite importo singola operaz.')
    quadro_bl3_limite_importo = \
        fields.Float(string='Quadro BL - Acquisti di servizi da soggetti \
                    non residenti - Limite importo')
    quadro_bl3_limite_importo_line = \
        fields.Float(string='Quadro BL - Acquisti di servizi da soggetti \
                    non residenti - Limite importo singola operaz.')
    quadro_se_limite_importo_line = \
        fields.Float(string='Quadro SE - Limite importo singola operaz.')

    @api.one
    def copy(self, default=None):
        default.update(anno=self.anno + 1)
        new_regole_ids = []
        for role in self.regole_ids:
            new_role = role.copy()
            new_regole_ids.append(new_role.id)
        if new_regole_ids:
            default['regole_ids'] = [(6, 0, new_regole_ids)]
        return super(spesometro_configurazione, self).copy(default)


class spesometro_regole(models.Model):

    @api.one
    @api.constrains('journal_id', 'account_id', 'partner_id')
    def _check_one_choose(self):
        if not self.journal_id\
                and not self.account_id\
                and not self.partner_id:
            raise ValidationError(
                _('Error Any filter setting! Journal, Account or Partner are \
                required '))

    _name = "spesometro.regole"
    _description = "Spesometro - Regole"

    configurazione_id = fields.Many2one('spesometro.configurazione',
                                        string='Configurazione', required=True, readonly=True)
    active = fields.Boolean('Active', default=True)
    note = fields.Text('Note')
    sequence = fields.Integer('Sequenza', required=True)
    move_id = fields.Many2one('account.move', 'Move')
    journal_id = fields.Many2one('account.journal', 'Journal')
    account_id = fields.Many2one('account.account', 'Account')
    partner_id = fields.Many2one('res.partner', 'Partner')
    counterpart_id = fields.Many2one('account.account', 'Counterpart')
    tipo_calcolo = fields.Selection((
        ('counterpart', 'Saldo Contropartita'),
        ('account_balance', 'Saldo Conto'),
        ('account_credit', 'Conto Avere'),
        ('account_debit', 'Conto Dare'),
        ('invoice', 'Fattura'),
        ('invoice_move', 'Registrazione Fattura'),
    ),
        'Tipo Calcolo', required=True)
    no_limite_importo = fields.Boolean('No limite importo')
    spesometro_partner_id = fields.Many2one('res.partner',
                                            'Partner sul quadro')
    spesometro_operazione = fields.Selection((
        ('FA', 'Quadro FA - Operazioni documentate da fattura'),
        ('SA', 'Quadro SA - Operazioni senza fattura'),
        ('BL1', 'Quadro BL - Operazioni con paesi con fiscalità privilegiata'),
        ('BL2', 'Quadro BL - Operazioni con soggetti non residenti'),
        ('BL3', 'Quadro BL - Acquisti di servizi da soggetti non residenti'),
        ('DR', 'Documento Riepilogativo')),
        'Operazione', required=True)
    spesometro_operazione_tipo_importo = fields.Selection((
        ('INE', 'Imponibile, Non Imponibile, Esente'),
        ('NS', 'Non Soggette ad IVA'),
        ('NV', 'Note di variazione')),
        'Tipo Importo')
    spesometro_segno = fields.Selection((('attiva', 'Attiva'),
                                         ('passiva', 'Passiva')),
                                        'Segno')
    spesometro_IVA_non_esposta = fields.Boolean('IVA non esposta')
    spesometro_leasing = fields.Selection((('A', 'Autovettura'),
                                           ('B', 'Caravan'),
                                           ('C', 'Altri veicoli'),
                                           ('D', 'Unità da diporto'),
                                           ('E', 'Aeromobili')),
                                          'Tipo Leasing')
    spesometro_tipo_servizio = fields.Selection((('cessione', 'Cessione Beni'),
                                                 ('servizi', 'Prestazione di servizi')), 'Tipo servizio',
                                                help="Specificare per 'Operazioni con soggetti non residenti' ")

    _order = "sequence"

    def get_importo(self, cr, uid, role_id, move):
        res = {
            'amount_untaxed': 0,
            'amount_tax': 0,
            'amount_total': 0,
        }

        invoice_obj = self.pool['account.invoice']
        move_line_obj = self.pool['account.move.line']
        if not role_id:
            return 0
        importo = 0
        move_line_ids = []
        role = self.browse(cr, uid, role_id)
        #
        # Calcolo da righe registrazione
        #
        if role.tipo_calcolo not in ['invoice', 'invoice_move']:
            # Selezione linee registrazione x calcolo
            if role.tipo_calcolo == 'counterpart':
                domain = [('move_id', '=', move.id),
                          ('account_id', '=', role.counterpart_id.id)]
                move_line_ids = move_line_obj.search(cr, uid, domain)
            elif role.tipo_calcolo == 'account_balance':
                domain = [('move_id', '=', move.id),
                          ('account_id', '=', role.account_id.id)]
                move_line_ids = move_line_obj.search(cr, uid, domain)
            elif role.tipo_calcolo == 'account_credit':
                domain = [('move_id', '=', move.id),
                          ('account_id', '=', role.account_id.id),
                          ('credit', '>', 0)]
                move_line_ids = move_line_obj.search(cr, uid, domain)
            elif role.tipo_calcolo == 'account_debit':
                domain = [('move_id', '=', move.id),
                          ('account_id', '=', role.account_id.id),
                          ('debit', '>', 0)]
                move_line_ids = move_line_obj.search(cr, uid, domain)
            # Calcolo
            for line in move_line_obj.browse(cr, uid, move_line_ids):
                if line.credit:
                    importo += line.credit
                else:
                    importo -= line.debit
            # if importo < 0:
            #    importo = importo * -1
            res['amount_total'] = round(importo, 2)
        #
        # Calcolo da fattura
        #
        elif role.tipo_calcolo == 'invoice':
            domain = [('move_id', '=', move.id)]
            inv_ids = invoice_obj.search(cr, uid, domain)
            if inv_ids:
                inv = invoice_obj.browse(cr, uid, inv_ids[0])
                for line in inv.tax_line:
                    if not line.tax_code_id.spesometro_escludi:
                        res['amount_untaxed'] += line.base
                        res['amount_tax'] += line.amount
                        res['amount_total'] += round(line.base +
                                                     line.amount, 2)
        #
        # Calcolo da registrazione contabile fattura
        #
        elif role.tipo_calcolo == 'invoice_move':
            for ml in move.line_id:
                # Iva
                domain = [('account_collected_id', '=', ml.account_id.id)]
                vat_acc_ids = self.pool['account.tax'].search(cr, uid, domain)
                if vat_acc_ids:
                    res['amount_tax'] += (ml.credit + ml.debit)
                # Credito/Debito (tot fattura)
                elif ml.account_id.type in ['payable', 'receivable']\
                        and ml.partner_id:
                    res['amount_total'] += (ml.credit + ml.debit)
            res['amount_untaxed'] = round(res['amount_total'] -
                                          res['amount_tax'], 2)

        return res

    def get_regola(self, cr, uid, move, invoice):
        '''
        Restituisce la prima regola valida seguendo la sequenza
        '''
        res = {}
        move_line_obj = self.pool['account.move.line']
        role_ids = self.search(cr, uid, [('active', '=', True)])
        for role in self.browse(cr, uid, role_ids):
            # test move
            if role.move_id \
                    and role.move_id.id != move.id:
                continue
            # test journal
            if role.journal_id \
                    and role.journal_id.id != move.journal_id.id:
                continue
            # test account
            if role.account_id:
                domain = [('move_id', '=', move.id),
                          ('account_id', '=', role.account_id.id)]
                move_line_ids = move_line_obj.search(cr, uid, domain)
                if not move_line_ids:
                    continue
            # test partner
            if role.partner_id:
                domain = [('move_id', '=', move.id),
                          ('partner_id', '=', role.partner_id.id)]
                move_line_ids = move_line_obj.search(cr, uid, domain)
                if not move_line_ids:
                    continue
            # test counterpart
            if role.counterpart_id:
                domain = [('move_id', '=', move.id),
                          ('account_id', '=', role.counterpart_id.id)]
                move_line_ids = move_line_obj.search(cr, uid, domain)
                if not move_line_ids:
                    continue
            #
            # La regola è ok: ricavo valori all'interno della registrazione
            #
            # Segno
            segno = role.spesometro_segno or False
            # ... Partner e segno(se non impostato)
            partner = False
            domain = [('move_id', '=', move.id)]
            if role.partner_id:
                domain.append(('partner_id', '=', role.partner_id.id))
            else:
                domain.append(('partner_id', '!=', False))
            move_line_ids = move_line_obj.search(cr, uid, domain, order='id')
            if not move_line_ids:
                continue
            move_line = move_line_obj.browse(cr, uid, move_line_ids[0])
            if role.spesometro_partner_id:
                partner = role.spesometro_partner_id
            else:
                partner = move_line.partner_id
            if not segno:
                for ml in move_line_obj.browse(cr, uid, move_line_ids):
                    if ml.account_id.type in ['other']:
                        continue
                    if ml.account_id.type in ['payable']:
                        segno = 'passiva'
                    elif ml.account_id.type in ['liquidity'] and ml.credit:
                        segno = 'passiva'
                    elif ml.account_id.type in ['liquidity'] and ml.debit:
                        segno = 'attiva'
                    else:
                        segno = 'attiva'
                    break
            # ... Calcolo importo
            res_importo = self.get_importo(cr, uid, role.id, move)
            res = {
                'role_id': role.id,
                'journal_id': role.journal_id and role.journal_id.id
                or False,
                'account_id': role.account_id and role.account_id.id
                or False,
                'counterpart_id': role.counterpart_id and
                role.counterpart_id.id or False,
                'partner_id': partner and partner.id or False,
                'segno': segno or False,
                'amount_untaxed': res_importo['amount_untaxed'],
                'amount_tax': res_importo['amount_tax'],
                'amount_total': res_importo['amount_total'],
                'operazione': role.spesometro_operazione,
                'operazione_tipo_importo':
                role.spesometro_operazione_tipo_importo,
                'tipo_servizio': role.spesometro_tipo_servizio,
                'no_limite_importo': role.no_limite_importo
            }
            break

        return res


class spesometro_comunicazione(models.Model):

    _name = "spesometro.comunicazione"
    _description = "Spesometro - Comunicazione "

    @api.model
    def _default_company(self):
        company_id = self._context.get('company_id',
                                       self.env.user.company_id.id)
        return company_id

    @api.model
    def _default_progressivo_telematico(self):
        com_next_prg = 1
        if self.tipo == 'ordinaria':
            domain = [('tipo', '=', 'ordinaria')]
            com_last = self.search(domain,
                                   order='progressivo_telematico desc',
                                   limit=1)
            if com_last:
                com_next_prg = com_last.progressivo_telematico + 1
        return com_next_prg

    @api.multi
    @api.depends('line_FA_ids', 'line_SA_ids', 'line_BL_ids', 'line_FE_ids',
                 'line_FR_ids', 'line_NE_ids', 'line_NR_ids', 'line_DF_ids',
                 'line_FN_ids', 'line_SE_ids', 'line_TU_ids')
    def _tot_operation_number(self):
        res = {}
        for com in self:
            # Aggregate
            tot_FA = len(com.line_FA_ids)
            tot_SA = len(com.line_SA_ids)
            tot_BL1 = 0
            tot_BL2 = 0
            tot_BL3 = 0
            for line in com.line_BL_ids:
                if line.operazione_fiscalita_privilegiata:
                    tot_BL1 += 1
                elif line.operazione_con_soggetti_non_residenti:
                    tot_BL2 += 1
                elif line.acquisto_servizi_da_soggetti_non_residenti:
                    tot_BL3 += 1
            # Analitiche
            tot_FE = 0  # Fatture emesse
            tot_FE_R = 0  # Doc riepilogativi
            for line in com.line_FE_ids:
                if line.documento_riepilogativo:
                    tot_FE_R += 1
                else:
                    tot_FE += 1
            tot_FR = 0  # Fatture ricevute
            tot_FR_R = 0  # Doc riepilogativi ricevuti
            for line in com.line_FR_ids:
                if line.documento_riepilogativo:
                    tot_FR_R += 1
                else:
                    tot_FR += 1
            tot_NE = len(com.line_NE_ids)
            tot_NR = len(com.line_NR_ids)
            tot_DF = len(com.line_DF_ids)
            tot_FN = len(com.line_FN_ids)
            tot_SE = len(com.line_SE_ids)
            tot_TU = len(com.line_TU_ids)
            # Write
            com.totale_FA = tot_FA
            com.totale_SA = tot_SA
            com.totale_BL1 = tot_BL1
            com.totale_BL2 = tot_BL2
            com.totale_BL3 = tot_BL3
            com.totale_FE = tot_FE
            com.totale_FE_R = tot_FE_R
            com.totale_FR = tot_FR
            com.totale_FR_R = tot_FR_R
            com.totale_NE = tot_NE
            com.totale_NR = tot_NR
            com.totale_DF = tot_DF
            com.totale_FN = tot_FN
            com.totale_SE = tot_SE
            com.totale_TU = tot_TU

    company_id = fields.Many2one('res.company', 'Azienda', required=True,
                                 default=_default_company)
    periodo = fields.Selection((('anno', 'Annuale'),
                                ('trimestre', 'Trimestrale'),
                                ('mese', 'Mensile')),
                               'Periodo', required=True, default='anno')
    anno = fields.Integer('Anno', size=4, required=True)
    trimestre = fields.Integer('Trimestre', size=1)
    mese = fields.Selection((('1', 'Gennaio'), ('2', 'Febbraio'), ('3', 'Marzo'),
                             ('4', 'Aprile'), ('5', 'Maggio'), ('6', 'Giugno'),
                             ('7', 'Luglio'), ('8',
                                               'Agosto'), ('9', 'Settembre'),
                             ('10', 'Ottobre'), ('11', 'Novembre'),
                             ('12', 'Dicembre'),
                             ), 'Mese')
    tipo = fields.Selection((('ordinaria', 'Ordinaria'),
                             ('sostitutiva', 'Sostitutiva'),
                             ('annullamento', 'Annullamento')),
                            'Tipo comunicazione', required=True,
                            default='ordinaria')
    comunicazione_da_sostituire_annullare = fields.Integer(
        'Protocollo comunicaz. da sostituire/annullare')
    documento_da_sostituire_annullare = fields.Integer(
        'Protocollo documento da sostituire/annullare')

    formato_dati = fields.Selection((('aggregati', 'Dati Aggregati'),
                                     ('analitici', 'Dati Analitici')),
                                    'Formato dati', default='aggregati')
    codice_fornitura = fields.Char('Codice fornitura',
                                   readonly=True, size=5,
                                   default='NSP00',
                                   help='Impostare a "NSP00" ')
    tipo_fornitore = fields.Selection((('01', 'Invio propria comunicazione'),
                                       ('10', 'Intermediario')),
                                      'Tipo fornitore',
                                      default='01')
    codice_fiscale_fornitore = fields.Char('Codice fiscale Fornitore', size=16,
                                           help="Deve essere uguale al Codice fiscale dell'intermediario \
        (campo 52 del record B) se presente, altrimenti al Codice fiscale del \
        soggetto tenuto alla comunicazione (campo 41 del record B) se \
        presente, altrimenti al Codice fiscale del soggetto obbligato \
        (campo 2 del record B)")
    #
    # Valori per comunicazione su più invii (non gestito)
    progressivo_telematico = fields.Integer('Progressivo telematico',
                                            default=_default_progressivo_telematico)
    numero_totale_invii = fields.Integer('Numero totale invii telematici',
                                         readonly=True)
    #
    # Soggetto a cui si riferisce la comunicazione
    #
    soggetto_codice_fiscale = fields.Char('Codice fiscale soggetto obbligato',
                                          size=16, help="Soggetto cui si riferisce la comunicazione")
    soggetto_partitaIVA = fields.Char('Partita IVA', size=11)
    soggetto_codice_attivita = fields.Char('Codice attività',
                                           size=6,
                                           help="Codice ATECO 2007")
    soggetto_telefono = fields.Char('Telefono', size=12)
    soggetto_fax = fields.Char('Fax', size=12)
    soggetto_email = fields.Char('E-mail', size=50)
    soggetto_forma_giuridica = fields.Selection((
        ('persona_giuridica', 'Persona Giuridica'),
        ('persona_fisica', 'Persona Fisica')),
        'Forma Giuridica')
    soggetto_codice_carica = fields.Selection((
        ('1', 'Rappresentante legale, negoziale o di fatto, socio \
            amministratore'),
        ('2', 'Rappresentante di minore, inabilitato o interdetto, ovvero \
            curatore dell’eredità giacente, amministratore di eredità \
            devoluta sotto condizione sospensiva o in favore di nascituro \
            non ancora concepito, amministratore di sostegno per le persone \
            con limitata capacità di agire'),
        ('3', 'Curatore fallimentare'),
        ('4', 'Commissario liquidatore (liquidazione coatta amministrativa \
            ovvero amministrazione straordinaria)'),
        ('5', 'Commissario giudiziale (amministrazione controllata) ovvero \
            custode giudiziario (custodia giudiziaria), ovvero \
            amministratore giudiziario in qualità di rappresentante dei beni \
            sequestrati'),
        ('6', 'Rappresentante fiscale di soggetto non residente'),
        ('7', 'Erede'),
        ('8', 'Liquidatore (liquidazione volontaria)'),
        ('9', 'Soggetto tenuto a presentare la dichiarazione ai fini IVA per \
            conto del soggetto estinto a seguito di operazioni straordinarie \
            o altre trasformazioni sostanziali soggettive (cessionario \
            d’azienda, società beneficiaria, incorporante, conferitaria, \
            ecc.); ovvero, ai fini delle imposte sui redditi e/o dell’IRAP, \
            rappresentante della società beneficiaria (scissione) o della \
            società risultante dalla fusione o incorporazione'),
        ('10', 'Rappresentante fiscale di soggetto non residente con le \
            limitazioni di cui all’art. 44, comma 3, del D.L. n. 331/1993'),
        ('11', 'Soggetto esercente l’attività tutoria del minore o interdetto \
            in relazione alla funzione istituzionale rivestita'),
        ('12', 'Liquidatore (liquidazione volontaria di ditta individuale - \
            periodo ante messa in liquidazione)'),
    ), 'Codice Carica')

    soggetto_pf_cognome = fields.Char('Cognome', size=24, help="")
    soggetto_pf_nome = fields.Char('Nome', size=20, help="")
    soggetto_pf_sesso = fields.Selection((('M', 'M'), ('F', 'F')), 'Sesso')
    soggetto_pf_data_nascita = fields.Date('Data di nascita')
    soggetto_pf_comune_nascita = fields.Char(
        'Comune o stato estero di nascita', size=40)
    soggetto_pf_provincia_nascita = fields.Char('Provincia', size=2)
    soggetto_pg_denominazione = fields.Char('Denominazione', size=60)

    # Soggetto tenuto alla comunicazione
    soggetto_cm_forma_giuridica = fields.Selection((
        ('persona_giuridica', 'Persona Giuridica'),
        ('persona_fisica', 'Persona Fisica')),
        'Forma Giuridica')
    soggetto_cm_codice_fiscale = fields.Char('Codice Fiscale', size=16,
                                             help="Soggetto che effettua la comunicazione se diverso dal soggetto \
        tenuto alla comunicazione")
    soggetto_cm_pf_cognome = fields.Char('Cognome', size=24, help="")
    soggetto_cm_pf_nome = fields.Char('Nome', size=20, help="")
    soggetto_cm_pf_sesso = fields.Selection((('M', 'M'), ('F', 'F')), 'Sesso')
    soggetto_cm_pf_data_nascita = fields.Date('Data di nascita')
    soggetto_cm_pf_comune_nascita = fields.Char(
        'Comune o stato estero di nascita', size=40)
    soggetto_cm_pf_provincia_nascita = fields.Char('Provincia', size=2)

    soggetto_cm_pf_data_inizio_procedura = fields.Date('Data inizio procedura')
    soggetto_cm_pf_data_fine_procedura = fields.Date('Data fine procedura')
    soggetto_cm_pg_denominazione = fields.Char('Denominazione', size=60)

    # Soggetto incaricato alla trasmissione
    soggetto_trasmissione_codice_fiscale = fields.Char(
        'Codice Fiscale', size=16,
        help="Intermediario che effettua la trasmissione telematica")
    soggetto_trasmissione_numero_CAF = fields.Integer(
        'Nr iscrizione albo del C.A.F.', size=5,
        help="Intermediario che effettua la trasmissione telematica")
    soggetto_trasmissione_impegno = fields.Selection((
        ('1', 'Soggetto obbligato'), ('2', 'Intermediario')),
        'Impegno trasmissione')
    soggetto_trasmissione_data_impegno = fields.Date('Data data impegno')

    quadro_FA = fields.Boolean(string='Quadro FA',
                               help="Operazioni documentate da fattura esposte in forma aggregata",
                               default=True)
    quadro_SA = fields.Boolean(string='Quadro SA',
                               help="Operazioni senza fattura esposte in forma aggregata",
                               default=True)
    quadro_BL = fields.Boolean(string='Quadro BL',
                               help="Operazioni con paesi con fiscalità privilegiata - \
        Operazioni con soggetti non residenti - \
        Acquisti di servizi da soggetti non residenti ", default=True)
    quadro_FE = fields.Boolean(string='Quadro FE',
                               help="Fatture emesse e Documenti riepilogativi (Operazioni attive)")
    quadro_FR = fields.Boolean(string='Quadro FR',
                               help="Fatture ricevute e Documenti riepilogativi (Operazioni passive)")
    quadro_NE = fields.Boolean(string='Quadro NE',
                               help="Note di variazione emesse")
    quadro_NR = fields.Boolean(string='Quadro NR',
                               help="Note di variazioni ricevute")
    quadro_DF = fields.Boolean(string='Quadro DF',
                               help="Operazioni senza fattura")
    quadro_FN = fields.Boolean(string='Quadro FN',
                               help="Operazioni con soggetti non residenti (Operazioni attive)")
    quadro_SE = fields.Boolean(string='Quadro SE',
                               help="Acquisti di servizi da non residenti e Acquisti da operatori di \
        San Marino", default=True)
    quadro_TU = fields.Boolean(string='Quadro TU',
                               help="Operazioni legate al turismo - Art. 3 comma 1 D.L. 16/2012")

    line_FA_ids = fields.One2many('spesometro.comunicazione.line.fa',
                                  'comunicazione_id', 'Quadri FA')
    line_SA_ids = fields.One2many('spesometro.comunicazione.line.sa',
                                  'comunicazione_id', 'Quadri SA')
    line_BL_ids = fields.One2many('spesometro.comunicazione.line.bl',
                                  'comunicazione_id', 'Quadri BL')

    line_FE_ids = fields.One2many('spesometro.comunicazione.line.fe',
                                  'comunicazione_id', 'Quadri FE')
    line_FR_ids = fields.One2many('spesometro.comunicazione.line.fr',
                                  'comunicazione_id', 'Quadri FR')
    line_NE_ids = fields.One2many('spesometro.comunicazione.line.ne',
                                  'comunicazione_id', 'Quadri NE')
    line_NR_ids = fields.One2many('spesometro.comunicazione.line.nr',
                                  'comunicazione_id', 'Quadri NR')
    line_DF_ids = fields.One2many('spesometro.comunicazione.line.df',
                                  'comunicazione_id', 'Quadri DF')
    line_FN_ids = fields.One2many('spesometro.comunicazione.line.fn',
                                  'comunicazione_id', 'Quadri FN')
    line_SE_ids = fields.One2many('spesometro.comunicazione.line.se',
                                  'comunicazione_id', 'Quadri SE')
    line_TU_ids = fields.One2many('spesometro.comunicazione.line.tu',
                                  'comunicazione_id', 'Quadri TU')

    totale_FA = fields.Integer(string='Tot operazioni FA',
                               compute='_tot_operation_number',
                               store=True, readonly=True)
    totale_SA = fields.Integer(string='Tot operazioni SA',
                               compute='_tot_operation_number',
                               store=True, readonly=True)
    totale_BL1 = fields.Integer(
        string='Tot operazioni BL - Paesi con fiscalita privilegiata',
        compute='_tot_operation_number', store=True, readonly=True)
    totale_BL2 = fields.Integer(
        string='Tot operazioni BL - Soggetti non residenti',
        compute='_tot_operation_number', store=True, readonly=True)
    totale_BL3 = fields.Integer(
        string='Tot operazioni BL - Acquisti servizi non soggetti non \
            residenti', compute='_tot_operation_number',
        store=True, readonly=True)

    totale_FE = fields.Integer(string='Tot operazioni FE',
                               compute='_tot_operation_number',
                               store=True, readonly=True)
    totale_FE_R = fields.Integer(string='Tot operazioni FE doc riepil.',
                                 compute='_tot_operation_number',
                                 store=True, readonly=True)
    totale_FR = fields.Integer(string='Tot operazioni FR',
                               compute='_tot_operation_number',
                               store=True, readonly=True)
    totale_FR_R = fields.Integer(string='Tot operazioni FR doc riepil.',
                                 compute='_tot_operation_number',
                                 store=True, readonly=True)
    totale_NE = fields.Integer(string='Tot operazioni NE',
                               compute='_tot_operation_number',
                               store=True, readonly=True)
    totale_NR = fields.Integer(string='Tot operazioni NR',
                               compute='_tot_operation_number',
                               store=True, readonly=True)
    totale_DF = fields.Integer(string='Tot operazioni DF',
                               compute='_tot_operation_number',
                               store=True, readonly=True)
    totale_FN = fields.Integer(string='Tot operazioni FN',
                               compute='_tot_operation_number',
                               store=True, readonly=True)
    totale_SE = fields.Integer(string='Tot operazioni SE',
                               compute='_tot_operation_number',
                               store=True, readonly=True)
    totale_TU = fields.Integer(string='Tot operazioni TU',
                               compute='_tot_operation_number',
                               store=True, readonly=True)

    @api.one
    def _unlink_sections(self):
        for line in self.line_FA_ids:
            line.unlink()
        for line in self.line_SA_ids:
            line.unlink()
        for line in self.line_BL_ids:
            line.unlink()
        for line in self.line_FE_ids:
            line.unlink()
        for line in self.line_FR_ids:
            line.unlink()
        for line in self.line_NE_ids:
            line.unlink()
        for line in self.line_NR_ids:
            line.unlink()
        for line in self.line_DF_ids:
            line.unlink()
        for line in self.line_FN_ids:
            line.unlink()
        for line in self.line_SE_ids:
            line.unlink()
        for line in self.line_TU_ids:
            line.unlink()

        return True

    @api.model
    def _get_quadri_richiesti(self):
        res = []
        if self.formato_dati == 'aggregati':
            if self.quadro_FA:
                res.append('FA')
            if self.quadro_SA:
                res.append('SA')
            if self.quadro_BL:
                res.append('BL')
        else:
            if self.quadro_FE:
                res.append('FE')
            if self.quadro_FR:
                res.append('FR')
            if self.quadro_NE:
                res.append('NE')
            if self.quadro_NR:
                res.append('NR')
            if self.quadro_DF:
                res.append('DF')
            if self.quadro_FN:
                res.append('FN')
            if self.quadro_SE:
                res.append('SE')
            if self.quadro_TU:
                res.append('TU')

        return res

    @api.onchange('soggetto_trasmissione_impegno')
    def onchange_soggetto_trasmissione_impegno(self):
        res = {}
        fiscalcode = False
        if self.soggetto_trasmissione_impegno == '1':  # soggetto obbligato
            fiscalcode = self._context.get('soggetto_codice_fiscale', False)
        self.soggetto_trasmissione_codice_fiscale = fiscalcode

    def partner_is_from_san_marino(self, move, invoice, arg):
        # configurazione
        anno_competenza = datetime.strptime(move.period_id.date_start,
                                            "%Y-%m-%d").year
        domain = [('anno', '=', anno_competenza)]
        configurazione = self.env['spesometro.configurazione'].search(domain)
        if not configurazione:
            raise ValidationError(_("Configurazione mancante! \
                Configurare l'anno relativo alla comunicazione"))

        stato_estero = False
        address = self._get_partner_address_obj(move, invoice, arg)
        if address and address.country_id and \
                configurazione.stato_san_marino.id == address.country_id.id:
            return True
        else:
            return False

    def _get_partner_address_obj(self, move, invoice, arg):
        address = False
        partner_address_obj = False
        # Partner
        if 'partner' in arg and arg['partner']:
            partner = arg['partner']
        else:
            partner = move.partner_id
        if partner.parent_id:
            partner_address_obj = partner.parent_id
        else:
            partner_address_obj = partner
        return partner_address_obj

    def _convert_only_number(self, cr, uid, string):
        if not string:
            string = ''
        string = ''.join(e for e in string if e.isdigit())
        return string

    def compute_amounts(self, move, invoice, arg):
        '''
        Calcolo totali documento. Dall'imponibile vanno esclusi gli importi 
        esclusi, fuori campo o esenti
        '''
        res = {
            'amount_untaxed': 0,
            'amount_tax': 0,
            'amount_total': 0,
        }
        if invoice:
            for line in invoice.tax_line:
                if not line.tax_code_id.spesometro_escludi:
                    res['amount_untaxed'] += line.base
                    res['amount_tax'] += line.amount
                    res['amount_total'] += round(line.base + line.amount, 2)
        else:
            regola = self.env['spesometro.regole'].get_regola(move,
                                                              invoice)
            if regola:
                res['amount_untaxed'] = regola['amount_untaxed']
                res['amount_tax'] = regola['amount_tax']
                res['amount_total'] = regola['amount_total']

        return res

    @api.one
    def truncate_values(self):
        for line in self.line_FA_ids:
            line.attive_imponibile_non_esente = \
                int(line.attive_imponibile_non_esente)
            line.attive_imposta = int(line.attive_imposta)
            line.attive_operazioni_iva_non_esposta = \
                int(line.attive_operazioni_iva_non_esposta)
            line.attive_note_variazione = int(line.attive_note_variazione)
            line.attive_note_variazione_imposta = \
                int(line.attive_note_variazione_imposta)

            line.passive_imponibile_non_esente = \
                int(line.passive_imponibile_non_esente)
            line.passive_imposta = int(line.passive_imposta)
            line.passive_operazioni_iva_non_esposta = \
                int(line.passive_operazioni_iva_non_esposta)
            line.passive_note_variazione = int(line.passive_note_variazione)
            line.passive_note_variazione_imposta = \
                int(line.passive_note_variazione_imposta)

        for line in self.line_SA_ids:
            line.importo_complessivo = int(line.importo_complessivo)

        for line in self.line_BL_ids:
            line.attive_importo_complessivo = \
                int(line.attive_importo_complessivo)
            line.attive_imposta = int(line.attive_imposta)
            line.attive_non_sogg_cessione_beni = \
                int(line.attive_non_sogg_cessione_beni)
            line.attive_non_sogg_servizi = \
                int(line.attive_non_sogg_servizi)
            line.attive_note_variazione = \
                int(line.attive_note_variazione)
            line.attive_note_variazione_imposta = \
                int(line.attive_note_variazione_imposta)

            line.passive_importo_complessivo = \
                int(line.passive_importo_complessivo)
            line.passive_imposta = int(line.passive_imposta)
            line.passive_non_sogg_importo_complessivo = \
                int(line.passive_non_sogg_importo_complessivo)
            line.passive_note_variazione = int(line.passive_note_variazione)
            line.passive_note_variazione_imposta = \
                int(line.passive_note_variazione_imposta)

        return True

    @api.one
    def validate_lines(self):

        # configurazione
        domain = [('anno', '=', self.anno)]
        configurazione = self.env['spesometro.configurazione'].search(domain)
        if not configurazione:
            raise ValidationError(_("Configurazione mancante! \
                Configurare l'anno relativo alla comunicazione"))

        for line in self.line_FA_ids:
            # Converto saldi negativi x casi di importi estrapolati dalla
            # contabilità
            importo_test = 0
            if line.attive_imponibile_non_esente:
                if line.attive_imponibile_non_esente < 0:
                    line.attive_imponibile_non_esente = \
                        line.attive_imponibile_non_esente * -1
                importo_test = line.attive_imponibile_non_esente
            if line.passive_imponibile_non_esente:
                if line.passive_imponibile_non_esente < 0:
                    line.passive_imponibile_non_esente = \
                        line.passive_imponibile_non_esente * -1
                importo_test = line.passive_imponibile_non_esente
            if configurazione.quadro_fa_limite_importo:
                if importo_test \
                    and (importo_test <
                         configurazione.quadro_fa_limite_importo):
                    line.unlink()

        for line in self.line_SA_ids:
            # Converto saldi negativi x casi di importi estrapolati dalla
            # contabilità
            if line.importo_complessivo < 0:
                line.importo_complessivo = line.importo_complessivo * -1
            if configurazione.quadro_sa_limite_importo:
                if line.importo_complessivo \
                    and (line.importo_complessivo <
                         configurazione.quadro_sa_limite_importo):
                    line.unlink()

        for line in self.line_BL_ids:

            importo_test = 0
            # operazioni attive
            if line.attive_importo_complessivo:
                importo_test = line.attive_importo_complessivo
            elif line.attive_non_sogg_cessione_beni:
                importo_test = line.attive_non_sogg_cessione_beni
            elif line.attive_non_sogg_servizi:
                importo_test = line.attive_non_sogg_servizi
            # operazioni passive
            elif line.passive_importo_complessivo:
                importo_test = line.passive_importo_complessivo
            elif line.passive_non_sogg_importo_complessivo:
                importo_test = line.passive_non_sogg_importo_complessivo

            to_remove = False
            # BL1 - Operazione con pesei con fiscalità privilegiata
            if line.operazione_fiscalita_privilegiata\
                    and configurazione.quadro_bl1_limite_importo:
                if importo_test < configurazione.quadro_bl1_limite_importo:
                    to_remove = True
            # BL2 - Operazione con soggetto non residente
            if line.operazione_con_soggetti_non_residenti\
                    and configurazione.quadro_bl2_limite_importo:
                if importo_test < configurazione.quadro_bl2_limite_importo:
                    to_remove = True
            # BL3 - Acquisto di servizi da soggetti non residenti
            if line.acquisto_servizi_da_soggetti_non_residenti\
                    and configurazione.quadro_bl3_limite_importo:
                if importo_test < configurazione.quadro_bl3_limite_importo:
                    to_remove = True

            if to_remove:
                line.unlink()

        # Controllo formale comunicazione
        # ... periodo in presenza di linee nel quadro SE
        if self.line_SE_ids and not self.trimestre and not self.mese:
            raise ValidationError(_("Perido Errato! In presenza di \
                operazione nel qudro SE (Acquisti da San Marino) sono \
                ammessi solo periodi mensili/trimestrali"))

        return True

    @api.model
    def validate_operation(self, move, invoice, arg):

        # configurazione
        anno_competenza = datetime.strptime(move.period_id.date_start,
                                            "%Y-%m-%d").year
        domain = [('anno', '=', anno_competenza)]
        configurazione = self.env['spesometro.configurazione'].search(domain)
        if not configurazione:
            raise ValidationError(_("Configurazione mancante! Configurare \
                l'anno relativo alla comunicazione"))

        doc_vals = self.env['spesometro.comunicazione'].compute_amounts(move,
                                                                        invoice,
                                                                        arg)
        # Nessu quadro definito
        if not arg['quadro']:
            return False
        # Quadro richiesto
        if arg['quadro'] not in arg['quadri_richiesti']:
            return False
        # Valori minimi
        # ... valori assoluti x confronti
        amount_total = doc_vals.get('amount_total', 0)
        if amount_total < 0:
            amount_total = amount_total * -1
        amount_untaxed = doc_vals.get('amount_untaxed', 0)
        if amount_untaxed < 0:
            amount_untaxed = amount_untaxed * -1

        # Nessun valore
        if not amount_total and not amount_untaxed:
            return False
        # Limiti
        if not arg['no_limite_importo']:
            if arg['quadro'] == 'FA':
                if configurazione.quadro_fa_limite_importo_line:
                    if not amount_untaxed or amount_untaxed < \
                            configurazione.quadro_fa_limite_importo_line:
                        return False
            if arg['quadro'] == 'SA':
                if configurazione.quadro_sa_limite_importo_line:
                    if not amount_total or amount_total < \
                            configurazione.quadro_sa_limite_importo_line:
                        return False
            if arg['quadro'] == 'BL':
                if arg['operazione'] == 'BL1':
                    if configurazione.quadro_bl1_limite_importo_line:
                        if not amount_total or amount_total < \
                                configurazione.quadro_bl1_limite_importo_line:
                            return False
                if arg['operazione'] == 'BL2':
                    if configurazione.quadro_bl2_limite_importo_line:
                        if not amount_total or amount_total < \
                                configurazione.quadro_bl2_limite_importo_line:
                            return False
                if arg['operazione'] == 'BL3':
                    if configurazione.quadro_bl3_limite_importo_line:
                        if not amount_total or amount_total < \
                                configurazione.quadro_bl3_limite_importo_line:
                            return False

            if arg['quadro'] == 'SE':
                if configurazione.quadro_se_limite_importo_line:
                    if not amount_untaxed or amount_untaxed < \
                            configurazione.quadro_se_limite_importo_line:
                        return False

        # Operazioni con San Marino Escluse se richiesta forma aggregata
        if arg['formato_dati'] == 'aggregati' and \
                self.partner_is_from_san_marino(move, invoice, arg):
            return False

        return True

    @api.model
    def _get_define_quadro(self, move, invoice, arg):

        quadro = False
        operazione = arg.get('operazione')
        # Forma aggregata
        if arg['formato_dati'] == 'aggregati':
            if operazione == 'FA' or operazione == 'DR':
                quadro = 'FA'
            elif operazione == 'SA':  # Operazioni senza fattura
                quadro = 'SA'
            elif operazione in ['BL1', 'BL2', 'BL3']:
                quadro = 'BL'

        # Forma analitica
        if arg['formato_dati'] == 'analitici':
            # Priorità x San Marino -> quadro SE
            if self.partner_is_from_san_marino(move, invoice, arg):
                operazione = 'BL3'
            # Impostazioni anagrafiche partner
            if operazione == 'FA' or operazione == 'DR':
                if arg.get('segno') == 'attiva':
                    quadro = 'FE'
                elif arg.get('segno') == 'passiva':
                    quadro = 'FR'
            # ... Operazioni senza fattura
            elif operazione == 'SA':
                quadro = 'DF'
            # ... Operazioni con soggetti non residenti
            elif operazione == 'BL2':
                quadro = 'FN'
            # ... Operazioni con paesi con fiscalità privilegiata -
            #        Acquisti di servizi da soggetti non residenti
            elif operazione == 'BL1' or operazione == 'BL3':
                quadro = 'SE'

            # Note di variazione
            if operazione == 'FE' and 'refund' in move.journal_id.type:
                operazione = 'NE'
            elif operazione == 'FR' and 'refund' in move.journal_id.type:
                operazione = 'NR'

        return quadro

    @api.model
    def _get_periods(self):
        '''
        Definizione periodi di competenza
        '''
        if not self.anno:
            raise ValidationError(_("Specificare l'anno della dichiarazione"))

        period_ids = []
        sql_select = "SELECT p.id FROM account_period p "
        sql_where = " WHERE p.special = False "
        search_params = {}
        # Company
        sql_where += " AND company_id = %(company_id)s "
        search_params.update({
            'company_id': self.company_id.id,
        })
        # Periodo annuale
        if self.periodo == 'anno':
            period_date_start = datetime(self.anno, 1, 1)
            period_date_stop = datetime(self.anno, 12, 31)
            sql_where += " AND p.date_start >= date(%(period_date_start)s) \
                AND p.date_stop <=date(%(period_date_stop)s) "
            search_params.update({
                'period_date_start': period_date_start,
                'period_date_stop': period_date_stop
            })
        # Periodo mensile
        if self.periodo == 'mese':
            period_date_start = datetime(self.anno, self.mese, 1)
            sql_where += " AND p.date_start = date(%(period_date_start)s) "
            search_params.update({
                'period_date_start': period_date_start,
            })
        # Periodo trimestrale
        if self.periodo == 'trimestre':
            if self.trimestre == 1:
                period_date_start = datetime(self.anno, 1, 1)
                period_date_stop = datetime(self.anno, 3, 31)
            elif self.trimestre == 2:
                period_date_start = datetime(self.anno, 3, 1)
                period_date_stop = datetime(self.anno, 6, 30)
            elif self.trimestre == 3:
                period_date_start = datetime(self.anno, 7, 1)
                period_date_stop = datetime(self.anno, 9, 30)
            elif self.trimestre == 4:
                period_date_start = datetime(self.anno, 10, 1)
                period_date_stop = datetime(self.anno, 12, 31)
            else:
                raise ValidationError(_("Errore nel valore del trimestre"))
            sql_where += " AND p.date_start >= date(%(period_date_start)s) \
                AND p.date_stop <=date(%(period_date_stop)s) "
            search_params.update({
                'period_date_start': period_date_start,
                'period_date_stop': period_date_stop
            })

        sql = sql_select + sql_where
        self.env.cr.execute(sql, search_params)
        period_ids = [i[0] for i in self.env.cr.fetchall()]

        return period_ids

    @api.onchange('tipo')
    def change_tipo(self):
        if self.tipo == 'ordinaria':
            domain = [('tipo', '=', 'ordinaria')]
            com_last = self.search(domain,
                                   order='progressivo_telematico desc',
                                   limit=1)
            com_next_prg = 1
            if com_last:
                com_next_prg = com_last.progressivo_telematico + 1
            self.progressivo_telematico = com_next_prg

    @api.onchange('tipo_fornitore')
    def change_tipo_fornitore(self):

        if self.tipo_fornitore == '01':
            self.soggetto_trasmissione_impegno = '2'
        else:
            self.soggetto_trasmissione_impegno = '1'

    @api.onchange('company_id')
    def change_company(self):
        # vat
        if self.company_id.partner_id.vat:
            self.soggetto_partitaIVA = self.company_id.partner_id.vat[2:]
        else:
            self.soggetto_partitaIVA = '{:11s}'.format("".zfill(11))
        # Fiscalcode
        self.soggetto_codice_fiscale = self.company_id.partner_id.fiscalcode \
            or ''
        # Personona fisica/giuridica
        if self.company_id.partner_id.fiscalcode and \
                len(self.company_id.partner_id.fiscalcode) < 16:
            self.soggetto_forma_giuridica = 'persona_giuridica'
            self.soggetto_pg_denominazione = self.company_id.partner_id.name
        else:
            self.soggetto_forma_giuridica = 'persona_fisica'

    @api.one
    def compute_statement(self):
        # Esistenza record di configurazione per l'anno della comunicazione
        domain = [('anno', '=', self.anno)]
        configurazione = self.env['spesometro.configurazione'].search(domain)
        if not configurazione:
            raise ValidationError(_("Configurazione mancante! Configurare \
                                    l'anno relativo alla comunicazione"))
        # Unlink existing lines
        self._unlink_sections()
        # quadri richiesti
        quadri_richiesti = self._get_quadri_richiesti()
        # periods
        period_ids = self._get_periods()
        # journal
        domain = [('spesometro', '=', True)]
        journals = self.env['account.journal'].search(domain)
        journal_ids = [journal.id for journal in journals]
        # Partners to exclude
        domain = [('spesometro_escludi', '=', True)]
        partners_to_exclude = self.env['res.partner'].search(domain)
        partner_to_exclude_ids = [pte.id for pte in partners_to_exclude]

        # Account moves
        domain = [('company_id', '=', self.company_id.id),
                  ('period_id', 'in', period_ids),
                  ('partner_id', 'not in', partner_to_exclude_ids)]
        account_moves = self.env['account.move'].search(domain)

        for move in account_moves:
            # Test move validate
            # ...evito di leggere tutti i movimenti se non sono impostate
            #    regole che possono prendere in considerazione movimenti senza
            #    partner
            if not configurazione.regole_ids \
                    and not move.partner_id:
                continue
            print "spesometro move > > " + str(move.id)

            # Invoice
            domain = [('move_id', '=', move.id)]
            invoice = self.env['account.invoice'].search(domain)
            # Partner
            partner = False
            if invoice:
                partner = invoice.partner_id
            elif move.partner_id:
                partner = move.partner_id
            else:
                domain = [('partner_id', '!=', False)]
                ml = self.env['account.move.line'].search(domain, limit=1)
                if ml:
                    partner = ml.partner_id

            # Config spesometro
            operazione = False
            tipo_servizio = False
            no_limite_importo = False
            operazione_iva_non_esposta = False
            operazione = move.journal_id.spesometro_operazione
            operazione_tipo_importo = \
                move.journal_id.spesometro_operazione_tipo_importo or False
            operazione_iva_non_esposta = \
                move.journal_id.spesometro_IVA_non_esposta
            segno = move.journal_id.spesometro_segno

            # Config spesometro - Da regole
            regola = self.env['spesometro.regole'].get_regola(move, invoice)
            if regola:
                if regola.get('operazione'):
                    operazione = regola.get('operazione')
                if regola.get('operazione_tipo_importo'):
                    operazione_tipo_importo = \
                        regola.get('operazione_tipo_importo')
                if regola.get('tipo_servizio'):
                    tipo_servizio = regola.get('tipo_servizio')
                if regola.get('segno'):
                    segno = regola.get('segno')
                if regola.get('partner_id'):
                    partner = self.env['res.partner'].browse(
                        regola['partner_id'])
                if regola.get('no_limite_importo'):
                    no_limite_importo = regola.get('no_limite_importo')

            # Salto movimento se:
            #   - Nessuna regola valida
            #   - La fattura appartiene ad un sezionale dove la
            #    comunicaz.art.21 non è configurata
            if invoice and not invoice.journal_id.id in journal_ids:
                continue
            if not invoice and not regola:
                continue

            # Config partner -> priorità alle impostazioni del partner
            if partner.spesometro_operazione:
                operazione = partner.spesometro_operazione
                operazione_tipo_importo = \
                    partner.spesometro_operazione_tipo_importo
                tipo_servizio = partner.spesometro_tipo_servizio
                operazione_iva_non_esposta = partner.spesometro_IVA_non_esposta

            arg = {
                'comunicazione_id': self.id,
                'partner': partner,
                'segno': segno,
                'operazione_iva_non_esposta': operazione_iva_non_esposta,
                'operazione': operazione,
                'operazione_tipo_importo': operazione_tipo_importo,
                'tipo_servizio': tipo_servizio,
                'no_limite_importo': no_limite_importo,
                'formato_dati': self.formato_dati,
                'quadri_richiesti': quadri_richiesti,
            }

            # Quadro di competenza
            quadro = self._get_define_quadro(move, invoice, arg)

            arg.update({'quadro': quadro})
            # Test operazione da includere nella comunicazione
            if not self.validate_operation(move, invoice, arg):
                continue
            if quadro == 'FA':
                line_id = self.env['spesometro.comunicazione.line.fa']\
                    .add_line(move, invoice, arg)
            if quadro == 'SA':
                line_id = self.env['spesometro.comunicazione.line.sa']\
                    .add_line(move, invoice, arg)
            if quadro == 'BL':
                line_id = self.env['spesometro.comunicazione.line.bl']\
                    .add_line(move, invoice, arg)
            if quadro == 'SE':
                line_id = self.env['spesometro.comunicazione.line.se']\
                    .add_line(move, invoice, arg)

        # Arrotonda importi su valori raggruppati -> troncare i decimali
        if self.formato_dati == 'aggregati':
            self.truncate_values()

        # Rimuove le linee che non rientrano nei limiti ed effettua un
        # controllo formale sull'intera comunicazione
        self.validate_lines()

    @api.model
    def _get_file_name(self):
        '''
        Formato Spesometro + Tipo + Periodo
        '''
        file_name = ''
        if self.periodo == 'mese':
            file_name = 'Spesometro%sM%s' % (str(self.anno), str(self.mese),)
        elif self.periodo == 'trimestre':
            file_name = 'Spesometro%sT%s' % (str(self.anno),
                                             str(self.trimestre),)
        else:
            file_name = 'Spesometro%s' % (str(self.anno),)
        return file_name

    @api.model
    def _split_string_positional_field(self, string):
        '''
        Da manuale:
        Con riferimento ai campi non posizionali, nel caso in cui la lunghezza 
        del dato da inserire ecceda i 16 caratteri disponibili, dovrà essere 
        inserito un ulteriore elemento con un identico campo-codice e con un 
        campo-valore il cui primo carattere dovrà essere impostato con il 
        simbolo “+”, mentre i successivi quindici potranno essere utilizzati 
        per la continuazione del dato da inserire. Tale situazione può 
        verificarsi solo per alcuni campi con formato AN.
        '''
        # Prima parte:
        res = []
        res.append(string[:16])
        length = 15
        # Parte in eccesso:
        str_eccesso = string[16:]
        str_split = [str_eccesso[i:i + length] for i in range(0, len(str_eccesso),
                                                              length)]
        for s in str_split:
            new_string = '+' + s
            res.append(new_string)
        return res

    @api.model
    def generate_file_export(self):
        '''
        Generazione contenuto del file da esportare
        '''
        content = ''
        numero_record_B = 0
        numero_record_C = 0
        numero_record_D = 0
        numero_record_E = 0

        # Testata
        content = self._record_A()
        numero_record_B += 1
        content += self._record_B()

        # Dettaglio
        progressivo_modulo = 0
        progressivo_sezione = 0
        sezione_max = 3
        # .. quadro FA
        for line in self.line_FA_ids:
            progressivo_modulo += 1
            progressivo_sezione += 1
            if progressivo_sezione > sezione_max:
                progressivo_sezione = 1
            content += self._record_C_FA(line, progressivo_modulo,
                                         progressivo_sezione)
            numero_record_C += 1
        # .. quadro SA
        progressivo_sezione = 0
        sezione_max = 10
        for line in self.line_SA_ids:
            progressivo_modulo += 1
            progressivo_sezione += 1
            if progressivo_sezione > sezione_max:
                progressivo_sezione = 1
            content += self._record_C_SA(line, progressivo_modulo,
                                         progressivo_sezione)
            numero_record_C += 1

        # .. quadro BL
        progressivo_sezione = 0
        sezione_max = 1
        for line in self.line_BL_ids:
            progressivo_modulo += 1
            progressivo_sezione += 1
            if progressivo_sezione > sezione_max:
                progressivo_sezione = 1
            content += self._record_C_BL(line, progressivo_modulo,
                                         progressivo_sezione)
            numero_record_C += 1

        # .. quadro SE
        progressivo_sezione = 0
        sezione_max = 3
        for line in self.line_SE_ids:
            progressivo_modulo += 1
            progressivo_sezione += 1
            if progressivo_sezione > sezione_max:
                progressivo_sezione = 1
            content += self._record_D_SE(line, progressivo_modulo,
                                         progressivo_sezione)
            numero_record_D += 1

        # Riepilogo
        progressivo_modulo = 1
        content += self._record_E(progressivo_modulo)
        numero_record_E += 1

        # Coda
        args = {
            'numero_record_B': numero_record_B,
            'numero_record_C': numero_record_C,
            'numero_record_D': numero_record_D,
            'numero_record_E': numero_record_E,
        }
        content += self._record_Z(args)
        # Validtation data
        if not content:
            raise ValidationError(
                _('Nothing to export'))

        return content

    def _record_A(self):

        if not self.soggetto_trasmissione_codice_fiscale:
            raise ValidationError(_("Errore comunicazione! Manca il codice \
                fiscale dell'incaricato alla trasmissione"))
        rcd = "A"
        rcd += '{:14s}'.format("")  # Filler
        rcd += "NSP00"  # codice fornitura
        # 01 - Soggetti che inviano la propria comunicazione 10 -Intermediari
        rcd += self.tipo_fornitore
        # cd fiscale  (se intermediaro va messo quello dell'intermediario)
        rcd += '{:16s}'.format(
            self.soggetto_trasmissione_codice_fiscale)
        rcd += '{:483s}'.format("")  # Filler
        # dich.su più invii: Progressivo dell'invio telematico
        rcd += '{:4s}'.format("0".zfill(4))
        # dich.su più invii: Numero totale degli invii telematici
        rcd += '{:4s}'.format("0".zfill(4))
        rcd += '{:100s}'.format("")  # Filler
        rcd += '{:1068s}'.format("")  # Filler
        rcd += '{:200s}'.format("")  # Filler
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r"  #
        rcd += "\n"  #

        return rcd

    def _record_B(self):

        if not self.soggetto_codice_fiscale:
            raise ValidationError(_("Errore comunicazione! Manca il codice\
                 fiscale del soggetto obbligato"))
        if not self.soggetto_codice_carica:
            raise ValidationError(_("Errore comunicazione! Manca il Codice \
                Carica del Soggetto "))

        rcd = "B"
        rcd += '{:16s}'.format(self.soggetto_codice_fiscale)
        rcd += '{:8s}'.format("1".zfill(8))  # Progressivo modulo - vale 1
        rcd += '{:3s}'.format("")  # Spazio a disposizione dell'utente
        rcd += '{:25s}'.format("")  # Filler
        rcd += '{:20s}'.format("")  # Spazio a disposizione dell'utente
        #  Identificativo del produttore del software (codice fiscale)
        rcd += '{:16s}'.format("")
        # tipo comunicazione (ordinaria,sostitutiva o di annullamento)
        if self.tipo == 'ordinaria':
            rcd += "1"
        else:
            rcd += "0"
        if self.tipo == 'sostitutiva':
            rcd += "1"
        else:
            rcd += "0"
        if self.tipo == 'annullamento':
            rcd += "1"
        else:
            rcd += "0"
        # campi x annullamento e sostituzione
        if self.comunicazione_da_sostituire_annullare == 0:
            rcd += '{:17s}'.format("".zfill(17))
        else:
            rcd += '{:17s}'.format(str(comunicazione_da_sostituire_annullare)
                                   .zfill(17))
        if self.documento_da_sostituire_annullare == 0:
            rcd += '{:6s}'.format("".zfill(6))
        else:
            rcd += '{:6s}'.format(str(self.documento_da_sostituire_annullare)
                                  .zfill(6))
        # formato dati: aggregata o analitica (caselle alternative)
        if self.formato_dati == 'aggregati':
            rcd += "10"
        else:
            rcd += "01"
        # Quadri compilati
        if self.line_FA_ids:
            rcd += "1"
        else:
            rcd += "0"
        if self.line_SA_ids:
            rcd += "1"
        else:
            rcd += "0"
        if self.line_BL_ids:
            rcd += "1"
        else:
            rcd += "0"
        # if comunicazione.quadro_FE :
        #     rcd += "1"
        # else:
        rcd += "0"
        # if comunicazione.quadro_FR :
        #     rcd += "1"
        # else:
        rcd += "0"
        # if comunicazione.quadro_NE :
        #     rcd += "1"
        # else:
        rcd += "0"
        # if comunicazione.quadro_NR :
        #     rcd += "1"
        # else:
        rcd += "0"
        # if comunicazione.quadro_DF :
        #     rcd += "1"
        # else:
        rcd += "0"
        # if comunicazione.quadro_FN :
        #     rcd += "1"
        # else:
        rcd += "0"
        if self.line_SE_ids:
            rcd += "1"
        else:
            rcd += "0"
        # if comunicazione.quadro_TU :
        #     rcd += "1"
        # else:
        rcd += "0"

        rcd += "1"  # Quadro TA  - RIEPILOGO
        # Partita IVA , Codice Attività e riferimenti del Soggetto cui si
        #  riferisce la comunicazione
        rcd += '{:11s}'.format(self.soggetto_partitaIVA)  # PARTITA IVA
        if not self.soggetto_codice_attivita:
            raise ValidationError(_("Errore comunicazione! Manca il \
                    codice attività"))
        # CODICE attività  (6 caratteri) --> obbligatorio
        rcd += '{:6s}'.format(self.soggetto_codice_attivita)
        tel = self.soggetto_telefono
        rcd += '{:12s}'.format(tel and tel.replace(' ', '') or '')  # telefono
        fax = self.soggetto_fax
        rcd += '{:12s}'.format(fax and fax.replace(' ', '') or '')  # fax
        rcd += '{:50s}'.format(self.soggetto_email or '')  # posta elettronica
        # Dati Anagrafici del Soggetto cui si riferisce la comunicazione
        # - Persona Fisica
        if self.soggetto_cm_codice_fiscale and \
                self.soggetto_cm_codice_fiscale == self.soggetto_codice_fiscale:
            raise ValidationError(_("Errore comunicazione! Codice fiscale del \
                soggetto tenuto Deve essere diverso da quello del soggetto \
                obbligato a cui si riferisce la comunicazione"))
        if self.soggetto_forma_giuridica == 'persona_fisica':
            if not self.soggetto_pf_cognome or not self.soggetto_pf_nome \
                    or not self.soggetto_pf_sesso \
                    or not self.soggetto_pf_data_nascita \
                    or not self.soggetto_pf_comune_nascita \
                    or not self.soggetto_pf_provincia_nascita:
                raise ValidationError(_("Soggetto obbligato: Inserire tutti i \
                    dati della persona fisica"))
            rcd += '{:24s}'.format(self.soggetto_pf_cognome)  # cognome
            rcd += '{:20s}'.format(self.soggetto_pf_nome)  # nome
            rcd += '{:1s}'.format(self.soggetto_pf_sesso)  # sesso
            rcd += '{:8s}'.format(datetime.strptime(
                self.soggetto_pf_data_nascita, "%Y-%m-%d").strftime("%d%m%Y"))
            rcd += '{:40s}'.format(self.soggetto_pf_comune_nascita)
            rcd += '{:2s}'.format(self.soggetto_pf_provincia_nascita)
            rcd += '{:60s}'.format("")  # persona giuridica
        else:
            if not self.soggetto_pg_denominazione:
                raise ValidationError(_("Soggetto obbligato: Inserire tutti \
                    i dati della persona giuridica"))
            rcd += '{:24s}'.format("")  # cognome
            rcd += '{:20s}'.format("")  # nome
            rcd += '{:1s}'.format("")  # sesso
            rcd += '{:8s}'.format("".zfill(8))  # data nascita
            rcd += '{:40s}'.format("")  # comune di nascita
            rcd += '{:2s}'.format("")  # provincia comune di nascita
            rcd += '{:60s}'.format(self.soggetto_pg_denominazione)

        rcd += '{:4d}'.format(self.anno)  #  anno riferimento
        #  Mese di riferimento : Da valorizzare obbligatoriamente solo se
        #  presenti Acquisti da Operatori di San Marino. In tutti gli altri casi
        #  non deve essere compilato
        if self.periodo == 'trimestre' and self.trimestre:
            rcd += '{:2s}'.format(str(self.trimestre) + "T")
        elif self.periodo == 'mese' and self.mese:
            rcd += '{:2s}'.format(str(self.mese).zfill(2))
        else:
            rcd += '{:2s}'.format("")
        # Dati del Soggetto tenuto alla comunicazione (soggetto che effettua
        # la comunicazione, se diverso dal soggetto cui si riferisce la
        # comunicazione)
        rcd += '{:16s}'.format(self.soggetto_cm_codice_fiscale or "")
        rcd += '{:2s}'.format(str(self.soggetto_codice_carica).zfill(2))
        rcd += '{:8s}'.format("".zfill(8))  # data inizio procedura
        rcd += '{:8s}'.format("".zfill(8))  #  data fine procedura
        # Dati anagrafici del soggetto tenuto alla comunicazione
        # - Persona fisica
        # (Obbligatorio e da compilare solo se si tratta di Persona Fisica. )
        if self.soggetto_cm_forma_giuridica == 'persona_fisica':
            if not self.soggetto_cm_pf_cognome \
                    or not self.soggetto_cm_pf_nome \
                    or not self.soggetto_cm_pf_sesso \
                    or not self.soggetto_cm_pf_data_nascita\
                    or not self.soggetto_cm_pf_comune_nascita \
                    or not self.soggetto_cm_pf_provincia_nascita:
                raise ValidationError(_("Soggetto tenuto alla \
                        comunicazione: Inserire tutti i dati della persona \
                        fisica"))
            rcd += '{:24s}'.format(self.soggetto_cm_pf_cognome)  # cognome
            rcd += '{:20s}'.format(self.soggetto_cm_pf_nome)  # nome
            rcd += '{:1s}'.format(self.soggetto_cm_pf_sesso)  # sesso
            rcd += '{:8s}'.format(datetime.strptime(
                self.soggetto_cm_pf_data_nascita,
                "%Y-%m-%d").strftime("%d%m%Y"))
            rcd += '{:40s}'.format(self.soggetto_cm_pf_comune_nascita)
            rcd += '{:2s}'.format(self.soggetto_cm_pf_provincia_nascita)
            rcd += '{:60s}'.format("")  #  persona giuridica
        #  - Persona giuridica
        else:
            if not self.soggetto_cm_pg_denominazione:
                raise ValidationError(_("Soggetto tenuto alla comunicazione: \
                    Inserire tutti i dati della persona giuridica"))
            rcd += '{:24s}'.format("")  # cognome
            rcd += '{:20s}'.format("")  # nome
            rcd += '{:1s}'.format("")  # sesso
            rcd += '{:8s}'.format("".zfill(8))  # data nascita
            rcd += '{:40s}'.format("")  # comune di nascita
            rcd += '{:2s}'.format("")  # provincia comune di nascita
            rcd += '{:60s}'.format(self.soggetto_cm_pg_denominazione)

        # Impegno alla trasmissione telematica
        if self.tipo_fornitore == '10' \
                and not self.soggetto_trasmissione_codice_fiscale:
            raise ValidationError(_("Manca il codice fiscale dell'intermediario\
                 incaricato alla trasmissione telematica"))
        # Codice fiscale dell'intermediario
        rcd += '{:16s}'.format(self.soggetto_trasmissione_codice_fiscale or '')
        # Numero di iscrizione all'albo del C.A.F.
        rcd += '{:5s}'.format(str(self.soggetto_trasmissione_numero_CAF)
                              .zfill(5))
        # Impegno a trasmettere in via telematica la comunicazione
        # Dato obbligatorio Vale 1 se la comunicazione è stata predisposta dal
        #  soggetto obbligato
        # Vale 2 se è stata predisposta dall'intermediario.
        rcd += '{:1s}'.format(self.soggetto_trasmissione_impegno)

        rcd += '{:1s}'.format("")  # Filler
        if not self.soggetto_trasmissione_data_impegno:
            raise ValidationError(_("Manca la data dell'impegno alla \
                trasmissione"))
        # Data dell'impegno
        rcd += '{:8s}'.format(datetime.strptime(
            self.soggetto_trasmissione_data_impegno,
            "%Y-%m-%d").strftime("%d%m%Y"))
        # Spazio riservato al Servizio telematico
        rcd += '{:1258s}'.format("")  # Filler
        rcd += '{:20s}'.format("")  # Spazio riservato al Servizio Telematico
        rcd += '{:18s}'.format("")  # Filler
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r"  #
        rcd += "\n"  #

        return rcd

    def _record_C_FA(self, line, prog_modulo, prog_sezione):
        prog_sezione = str(prog_sezione).zfill(3)

        rcd = "C"
        # codice fiscale soggetto obbligato
        rcd += '{:16s}'.format(line.comunicazione_id.soggetto_codice_fiscale)
        rcd += '{:8s}'.format(str(prog_modulo).zfill(8))  # Progressivo modulo
        rcd += '{:3s}'.format("")  # Filler
        rcd += '{:25s}'.format("")  # Filler
        rcd += '{:20s}'.format("")  # Spazio utente
        rcd += '{:16s}'.format("")  # Filler

        # QUADRO FA
        # Partita iva o codice fiscale presenti se non si tratta di documento
        # riepilogativo (ES: scheda carburante)
        if not line.partita_iva and not line.codice_fiscale \
                and not line.documento_riepilogativo:
            raise ValidationError(_("Inserire Codice Fiscale o partita IVA su\
                 partner %s") % (line.partner_id.name,))
        # Doc. riepilogativo : non ammessi codice fiscale o partita iva
        if line.documento_riepilogativo \
                and (line.partita_iva or line.codice_fiscale):
            raise ValidationError(_("Documento riepilogativo per partner %s, \
                togliere Codice Fiscale E partita IVA")
                                  % (line.partner_id.name,))

        if line.partita_iva:
            rcd += '{:8s}'.format("FA" + prog_sezione + "001")
            rcd += '{:16s}'.format(line.partita_iva)
        elif line.codice_fiscale:
            rcd += '{:8s}'.format("FA" + prog_sezione + "002")
            rcd += '{:16s}'.format(line.codice_fiscale)
        if line.documento_riepilogativo:
            rcd += '{:8s}'.format("FA" + prog_sezione + "003") \
                + '{:>16s}'.format('1')
        # Numero operazioni attive aggregate
        if line.numero_operazioni_attive_aggregate > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "004") \
                + '{:16d}'.format(line.numero_operazioni_attive_aggregate)
        # Numero operazioni passive aggregate
        if line.numero_operazioni_passive_aggregate > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "005") \
                + '{:16d}'.format(line.numero_operazioni_passive_aggregate)
        # Noleggio / Leasing
        if line.noleggio:
            rcd += '{:8s}'.format("FA" + prog_sezione + "006") \
                + '{:16s}'.format(line.noleggio)

        # OPERAZIONI ATTIVE
        if line.attive_imponibile_non_esente > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "007") \
                + '{:16.0f}'.format(line.attive_imponibile_non_esente)
        # Totale imposta
        if line.attive_imposta > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "008") \
                + '{:16.0f}'.format(line.attive_imposta)
        # Totale operazioni con IVA non esposta
        if line.attive_operazioni_iva_non_esposta > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "009") \
                + '{:16.0f}'.format(line.attive_operazioni_iva_non_esposta)
        # Totale note di variazione a debito per la controparte
        if line.attive_note_variazione > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "010") \
                + '{:16.0f}'.format(line.attive_note_variazione)
        if line.attive_note_variazione_imposta > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "011") \
                + '{:16.0f}'.format(line.attive_note_variazione_imposta)

        # OPERAZIONI PASSIVE
        # Totale operazioni imponibili, non imponibili ed esenti
        if line.passive_imponibile_non_esente > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "012") \
                + '{:16.0f}'.format(line.passive_imponibile_non_esente)
        if line.passive_imposta > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "013") \
                + '{:16.0f}'.format(line.passive_imposta)
        if line.passive_operazioni_iva_non_esposta > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "014") \
                + '{:16.0f}'.format(line.passive_operazioni_iva_non_esposta)
        if line.passive_note_variazione > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "015") \
                + '{:16.0f}'.format(line.passive_note_variazione)
        if line.passive_note_variazione_imposta > 0:
            rcd += '{:8s}'.format("FA" + prog_sezione + "016") \
                + '{:16.0f}'.format(line.passive_note_variazione_imposta)

        # riempio fino a 1900 caratteri
        rcd += " " * (1897 - len(rcd))
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r"  #
        rcd += "\n"  #

        return rcd

    def _record_C_SA(self, line, prog_modulo, prog_sezione):
        prog_sezione = str(prog_sezione).zfill(3)

        if not line.codice_fiscale:
            raise ValidationError(_("Manca codice fiscale su partner %s")
                                  % (line.partner_id.name,))
        rcd = "C"
        # codice fiscale soggetto obbligato
        rcd += '{:16s}'.format(line.comunicazione_id.soggetto_codice_fiscale)
        rcd += '{:8s}'.format(str(prog_modulo).zfill(8))  # Progressivo modulo
        rcd += '{:3s}'.format("")  # Filler
        rcd += '{:25s}'.format("")  # Filler
        rcd += '{:20s}'.format("")  # Spazio utente
        rcd += '{:16s}'.format("")  # Filler

        rcd += '{:8s}'.format("SA" + prog_sezione + "001") \
            + '{:16s}'.format(line.codice_fiscale)
        if line.numero_operazioni:
            rcd += '{:8s}'.format("SA" + prog_sezione + "002") \
                + '{:16d}'.format(line.numero_operazioni)
        if line.importo_complessivo:
            rcd += '{:8s}'.format("SA" + prog_sezione + "003") \
                + '{:16.0f}'.format(line.importo_complessivo)
        if line.noleggio:
            rcd += '{:8s}'.format("SA" + prog_sezione + "004") \
                + '{:16s}'.format(line.noleggio)

        # riempio fino a 1900 caratteri
        rcd += " " * (1897 - len(rcd))
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r"  #
        rcd += "\n"  #

        return rcd

    def _record_C_BL(self, line, prog_modulo, prog_sezione, context=None):

        prog_sezione = str(prog_sezione).zfill(3)

        # Controlli
        # ...Operazioni con paesi con fiscalità privilegiata (è obbligatorio
        #     compilare le sezioni BL001, BL002 e almeno un campo delle sezioni
        #     BL003, BL004, BL005, BL006, BL007, BL008)
        if line.operazione_fiscalita_privilegiata:
            if (not line.pf_cognome or not line.pf_nome) \
                    and not line.pg_denominazione:
                ValidationError(_("Errore quadro BL - Partner %s! Cognome e \
                    nome obbligatori oppure ragione sociale per soggetto \
                    giuridico") % (line.partner_id.name,))
        # ...Operazioni con soggetti non residenti (è obbligatorio compilare
        #    le sezioni BL001, BL002 e almeno un campo delle sezioni BL003 e
        #    BL006)
        if line.operazione_con_soggetti_non_residenti:
            if (not line.pf_cognome or not line.pf_nome) \
                    and not line.pg_denominazione:
                ValidationError("Errore quadro BL - Partner %s! Cognome e nome\
                     obbligatori oppure ragione sociale per soggetto \
                     giuridico") % (line.partner_id.name,)
            if line.pf_cognome and not line.pf_data_nascita \
                    and not line.pf_codice_stato_estero:
                raise ValidationError(_("Errore quadro BL - Partner %s! \
                    Inserire alemno uno dei seguenti valori: \
                    Pers.Fisica-Data di nascita, Pers.Fisica-Codice Stato")
                                      % (line.partner_id.name,))
        # ...Acquisti di servizi da soggetti non residenti (è obbligatorio
        #    compilare le sezioni BL001, BL002 e almeno un campo della sezione
        #    BL006)
        if line.acquisto_servizi_da_soggetti_non_residenti:
            if (not line.pf_cognome or not line.pf_nome) \
                    and not line.pg_denominazione:
                raise ValidationError(_("Errore quadro BL - Partner %s! \
                    Cognome e nome obbligatori oppure ragione sociale per \
                    soggetto giuridico") % (line.partner_id.name,))
            if line.pf_cognome and not line.pf_data_nascita \
                    and not line.pf_codice_stato_estero:
                raise ValidationError(_("Errore quadro BL - Partner %s! \
                    Inserire alemno uno dei seguenti valori: \
                    Pers.Fisica-Data di nascita, Pers.Fisica-Codice Stato")
                                      % (line.partner_id.name,))
        # BL001006 : Codice stato estero x persona fisica
        if not line.pg_denominazione and not line.pf_codice_stato_estero:
            raise ValidationError(_("Errore quadro BL - Partner %s! \
                    Inserire Codice Stato Estero per la persona fisica")
                                  % (line.partner_id.name,))
        # BL001009 : Codice stato estero x persona giuridica
        if line.pg_denominazione and not line.pg_codice_stato_estero:
            raise ValidationError(_("Errore quadro BL - Partner %s! \
                    Inserire Codice Stato Estero per la persona giuridica")
                                  % (line.partner_id.name,))

        rcd = "C"
        # codice fiscale soggetto obbligato
        rcd += '{:16s}'.format(line.comunicazione_id.soggetto_codice_fiscale)
        rcd += '{:8s}'.format(str(prog_modulo).zfill(8))  # Progressivo modulo
        rcd += '{:3s}'.format("")  # Filler
        rcd += '{:25s}'.format("")  # Filler
        rcd += '{:20s}'.format("")  # Spazio utente
        rcd += '{:16s}'.format("")  # Filler

        # Dati anagrafici
        # .. persona fisica
        if line.pf_cognome:
            if not line.pf_nome or not line.pf_data_nascita \
                    or not line.pf_comune_stato_nascita \
                    or not line.pf_provincia_nascita \
                    or not line.pf_codice_stato_estero:
                raise ValidationError(_('Completare dati persona fisica nel \
                    quadro BL del partner: %s') % (line.partner_id.name,))
            str_split = self._split_string_positional_field(line.pf_cognome)
            for s in str_split:
                rcd += '{:8s}'.format("BL" + "001" + "001") \
                    + '{:16s}'.format(s)
            str_split = self._split_string_positional_field(line.pf_nome)
            for s in str_split:
                rcd += '{:8s}'.format("BL" + "001" + "002")  \
                    + '{:16s}'.format(s)
            rcd += '{:8s}'.format("BL" + "001" + "003") \
                + '{:>16s}'.format(datetime.strptime(
                    line.pf_data_nascita, "%Y-%m-%d").strftime("%d%m%Y"))
            str_split = self._split_string_positional_field(
                line.pf_comune_stato_nascita)
            for s in str_split:
                rcd += '{:8s}'.format("BL" + "001" + "004") \
                    + '{:16s}'.format(s)
            rcd += '{:8s}'.format("BL" + "001" + "005") \
                + '{:16s}'.format(line.pf_provincia_nascita)
            rcd += '{:8s}'.format("BL" + "001" + "006") \
                + '{:>16s}'.format(line.pf_codice_stato_estero)
        # .. persona giuridica
        if line.pg_denominazione:
            if not line.pg_citta_estera_sede_legale \
                    or not line.pg_codice_stato_estero \
                    or not line.pg_indirizzo_sede_legale:
                raise ValidationError(_('Completare dati persona giuridica \
                    nel quadro BL del partner: %s : Citta estera - Codice \
                    Stato estero - Indirizzo') % (line.partner_id.name,))
            str_split = self._split_string_positional_field(
                line.pg_denominazione)
            for s in str_split:
                rcd += '{:8s}'.format("BL" + "001" + "007") \
                    + '{:16s}'.format(s)
            str_split = self._split_string_positional_field(
                line.pg_citta_estera_sede_legale)
            for s in str_split:
                rcd += '{:8s}'.format("BL" + "001" + "008") \
                    + '{:16s}'.format(s)
            rcd += '{:8s}'.format("BL" + "001" + "009") \
                + '{:>16s}'.format(line.pg_codice_stato_estero)
            str_split = self._split_string_positional_field(
                line.pg_indirizzo_sede_legale)
            for s in str_split:
                rcd += '{:8s}'.format("BL" + "001" + "010") \
                    + '{:16s}'.format(s)
        # Codice identificativo IVA
        if line.codice_identificativo_IVA:
            rcd += '{:8s}'.format("BL" + "002" + "001") \
                + '{:16s}'.format(line.codice_identificativo_IVA or '')
        # Operazioni con paesi con fiscalità privilegiata
        rcd += '{:8s}'.format("BL" + "002" + "002")
        if line.operazione_fiscalita_privilegiata:
            rcd += '{:>16s}'.format("1")
        else:
            rcd += '{:>16s}'.format("0")
        # Operazioni con soggetti non residenti
        rcd += '{:8s}'.format("BL" + "002" + "003")
        if line.operazione_con_soggetti_non_residenti:
            rcd += '{:>16s}'.format("1")
        else:
            rcd += '{:>16s}'.format("0")
        # Acquisti di servizi da soggetti non residenti
        rcd += '{:8s}'.format("BL" + "002" + "004")
        if line.acquisto_servizi_da_soggetti_non_residenti:
            rcd += '{:>16s}'.format("1")
        else:
            rcd += '{:>16s}'.format("0")

        # OPERAZIONI ATTIVE
        if line.attive_importo_complessivo > 0:
            rcd += '{:8s}'.format("BL" + "003" + "001") \
                + '{:16.0f}'.format(line.attive_importo_complessivo)
        if line.attive_imposta > 0:
            rcd += '{:8s}'.format("BL" + "003" + "002") \
                + '{:16.0f}'.format(line.attive_imposta)

        if line.attive_non_sogg_cessione_beni > 0:
            rcd += '{:8s}'.format("BL" + "004" + "001") \
                + '{:16.0f}'.format(line.attive_non_sogg_cessione_beni)
        if line.attive_non_sogg_servizi > 0:
            rcd += '{:8s}'.format("BL" + "004" + "002") \
                + '{:16.0f}'.format(line.attive_non_sogg_servizi)
        if line.attive_note_variazione > 0:
            rcd += '{:8s}'.format("BL" + "005" + "001") \
                + '{:16.0f}'.format(line.attive_note_variazione)
        if line.attive_note_variazione_imposta > 0:
            rcd += '{:8s}'.format("BL" + "005" + "002") \
                + '{:16.0f}'.format(line.attive_note_variazione_imposta)

        # OPERAZIONI PASSIVE
        if line.passive_importo_complessivo > 0:
            rcd += '{:8s}'.format("BL" + "006" + "001") \
                + '{:16.0f}'.format(line.passive_importo_complessivo)
        if line.passive_imposta > 0:
            rcd += '{:8s}'.format("BL" + "006" + "002") \
                + '{:16.0f}'.format(line.passive_imposta)

        if line.passive_non_sogg_importo_complessivo > 0:
            rcd += '{:8s}'.format("BL" + "007" + "001") \
                + '{:16.0f}'.format(line.passive_non_sogg_importo_complessivo)
        if line.passive_note_variazione > 0:
            rcd += '{:8s}'.format("BL" + "008" + "001") \
                + '{:16.0f}'.format(line.passive_note_variazione)
        if line.passive_note_variazione_imposta > 0:
            rcd += '{:8s}'.format("BL" + "008" + "002") \
                + '{:16.0f}'.format(line.passive_note_variazione_imposta)

        # riempio fino a 1900 caratteri
        rcd += " " * (1897 - len(rcd))
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r"  #
        rcd += "\n"  #

        return rcd

    def _record_D_SE(self, line, prog_modulo, prog_sezione, context=None):

        prog_sezione = str(prog_sezione).zfill(3)

        # Controlli
        # ...Cognome o Ragione sociale
        if (not line.pf_cognome or not line.pf_nome) \
                and not line.pg_denominazione:
            raise ValidationError(_("Errore quadro SE - Partner %s! Cognome \
                e nome obbligatori oppure ragione sociale per soggetto \
                giuridico") % (line.partner_id.name,))
        # ...
        if line.pf_cognome and not line.pf_data_nascita \
                and not line.pf_codice_stato_estero:
            raise ValidationError(_("Errore quadro SE - Partner %s! Inserire \
                alemno uno dei seguenti valori: \
                Pers.Fisica-Data di nascita, Pers.Fisica-Codice Stato")
                                  % (line.partner_id.name,))

        rcd = "D"
        # codice fiscale soggetto obbligato
        rcd += '{:16s}'.format(line.comunicazione_id.soggetto_codice_fiscale)
        rcd += '{:8s}'.format(str(prog_modulo).zfill(8))  # Progressivo modulo
        rcd += '{:3s}'.format("")  # Filler
        rcd += '{:25s}'.format("")  # Filler
        rcd += '{:20s}'.format("")  # Spazio utente
        rcd += '{:16s}'.format("")  # Filler

        # Dati anagrafici
        # .. persona fisica
        if line.pf_cognome:
            if not line.pf_nome or not line.pf_data_nascita \
                    or not line.pf_comune_stato_nascita \
                    or not line.pf_provincia_nascita \
                    or not line.pf_codice_stato_estero:
                raise ValidationError(_('Completare dati persona fisica nel \
                    quadro SE del partner: %s') % (line.partner_id.name,))
            str_split = self._split_string_positional_field(line.pf_cognome)
            for s in str_split:
                rcd += '{:8s}'.format("SE" + prog_sezione + "001") \
                    + '{:16s}'.format(s)
            str_split = self._split_string_positional_field(line.pf_nome)
            for s in str_split:
                rcd += '{:8s}'.format("SE" + prog_sezione + "002")  \
                    + '{:16s}'.format(s)
            rcd += '{:8s}'.format("SE" + prog_sezione + "003") \
                + '{:16s}'.format(datetime.strptime(
                    line.pf_data_nascita, "%Y-%m-%d").strftime("%d%m%Y"))
            str_split = self._split_string_positional_field(
                line.pf_comune_stato_nascita)
            for s in str_split:
                rcd += '{:8s}'.format("SE" + prog_sezione + "004") \
                    + '{:16s}'.format(s)
            rcd += '{:8s}'.format("SE" + prog_sezione + "005") \
                + '{:16s}'.format(line.pf_provincia_nascita)
            rcd += '{:8s}'.format("SE" + prog_sezione + "006") \
                + '{:>16s}'.format(line.pf_codice_stato_estero_domicilio)
        # .. persona giuridica
        if line.pg_denominazione:
            if not line.pg_citta_estera_sede_legale \
                    or not line.pg_codice_stato_estero_domicilio \
                    or not line.pg_indirizzo_sede_legale:
                raise ValidationError(_('Completare dati persona giuridica nel\
                     quadro SE del partner: %s : Citta estera - Codice Stato \
                     estero - Indirizzo') % (line.partner_id.name,))
            str_split = self._split_string_positional_field(
                line.pg_denominazione)
            for s in str_split:
                rcd += '{:8s}'.format("SE" + prog_sezione + "007") \
                    + '{:16s}'.format(s)
            str_split = self._split_string_positional_field(
                line.pg_citta_estera_sede_legale)
            for s in str_split:
                rcd += '{:8s}'.format("SE" + prog_sezione + "008") \
                    + '{:16s}'.format(s)
            rcd += '{:8s}'.format("SE" + prog_sezione + "009") \
                + '{:>16s}'.format(line.pg_codice_stato_estero_domicilio)
            str_split = self._split_string_positional_field(
                line.pg_indirizzo_sede_legale)
            for s in str_split:
                rcd += '{:8s}'.format("SE" + prog_sezione + "010") \
                    + '{:16s}'.format(s)
        # Codice identificativo IVA
        if line.codice_identificativo_IVA:
            rcd += '{:8s}'.format("SE" + prog_sezione + "011") \
                + '{:16s}'.format(line.codice_identificativo_IVA)
        # Dati documento
        rcd += '{:8s}'.format("SE" + prog_sezione + "012") \
            + '{:>16s}'.format(datetime.strptime(line.data_emissione,
                                                 "%Y-%m-%d").strftime("%d%m%Y"))
        rcd += '{:8s}'.format("SE" + prog_sezione + "013") \
            + '{:>16s}'.format(datetime.strptime(
                line.data_registrazione, "%Y-%m-%d").strftime("%d%m%Y"))
        rcd += '{:8s}'.format("SE" + prog_sezione + "014") \
            + '{:16s}'.format(line.numero_fattura)

        if line.importo > 0:
            rcd += '{:8s}'.format("SE" + prog_sezione + "015") \
                + '{:16.0f}'.format(line.importo)
        if line.imposta > 0:
            rcd += '{:8s}'.format("SE" + prog_sezione + "016") \
                + '{:16.0f}'.format(line.imposta)

        # riempio fino a 1900 caratteri
        rcd += " " * (1897 - len(rcd))
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r"  #
        rcd += "\n"  #

        return rcd

    def _record_E(self, prog_modulo):
        rcd = "E"
        rcd += '{:16s}'.format(self.soggetto_codice_fiscale)
        # rcd += '{:8d}'.format(prog_modulo) # Progressivo modulo
        rcd += '{:8s}'.format(str(prog_modulo).zfill(8))  # Progressivo modulo
        rcd += '{:3s}'.format("")  # Filler
        rcd += '{:25s}'.format("")  # Filler
        rcd += '{:20s}'.format("")  # Filler
        rcd += '{:16s}'.format("")  # Filler
        # Aggregate
        if self.totale_FA:
            rcd += '{:8s}'.format("TA001001") + '{:16d}'.format(self.totale_FA)
        if self.totale_SA:
            rcd += '{:8s}'.format("TA002001") + '{:16d}'.format(self.totale_SA)
        if self.totale_BL1:
            rcd += '{:8s}'.format("TA003001") + \
                '{:16d}'.format(self.totale_BL1)
        if self.totale_BL2:
            rcd += '{:8s}'.format("TA003002") + \
                '{:16d}'.format(self.totale_BL2)
        if self.totale_BL3:
            rcd += '{:8s}'.format("TA003003") + \
                '{:16d}'.format(self.totale_BL3)
        # Analitiche
        if self.totale_FE:
            rcd += '{:8s}'.format("TA004001") + '{:16d}'.format(self.totale_FE)
        if self.totale_FE_R:
            rcd += '{:8s}'.format("TA004002") \
                + '{:16d}'.format(self.totale_FE_R)
        if self.totale_FR:
            rcd += '{:8s}'.format("TA005001") + '{:16d}'.format(self.totale_FR)
        if self.totale_FR_R:
            rcd += '{:8s}'.format("TA005002") \
                + '{:16d}'.format(self.totale_FR_R)
        if self.totale_NE:
            rcd += '{:8s}'.format("TA006001") + '{:16d}'.format(self.totale_NE)
        if self.totale_NR:
            rcd += '{:8s}'.format("TA007001") + '{:16d}'.format(self.totale_NR)
        if self.totale_DF:
            rcd += '{:8s}'.format("TA008001") + '{:16d}'.format(self.totale_DF)
        if self.totale_FN:
            rcd += '{:8s}'.format("TA009001") + '{:16d}'.format(self.totale_FN)
        if self.totale_SE:
            rcd += '{:8s}'.format("TA010001") + '{:16d}'.format(self.totale_SE)
        if self.totale_TU:
            rcd += '{:8s}'.format("TA011001") + '{:16d}'.format(self.totale_TU)

        rcd += " " * (1897 - len(rcd))

        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r"  #
        rcd += "\n"  #
        return rcd

    def _record_Z(self, args):
        rcd = "Z"
        rcd += '{:14s}'.format("")  #  filler
        rcd += '{:9s}'.format(str(args.get('numero_record_B')).zfill(9))
        rcd += '{:9s}'.format(str(args.get('numero_record_C')).zfill(9))
        rcd += '{:9s}'.format(str(args.get('numero_record_D')).zfill(9))
        rcd += '{:9s}'.format(str(args.get('numero_record_E')).zfill(9))
        rcd += " " * 1846
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r"  #
        rcd += "\n"  #
        return rcd


class spesometro_comunicazione_line_FA(models.Model):
    '''
    QUADRO FA - Operazioni documentate da fattura esposte in forma aggregata
    '''

    _name = "spesometro.comunicazione.line.fa"
    _description = "Spesometro - Comunicazione linee quadro FA"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione',
                                       ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner')
    partita_iva = fields.Char('Partita IVA', size=11)
    codice_fiscale = fields.Char('Codice Fiscale', size=16)
    documento_riepilogativo = fields.Boolean('Documento Riepilogativo')
    noleggio = fields.Selection((('A', 'Autovettura'),
                                 ('B', 'Caravan'),
                                 ('C', 'Altri Veicoli'),
                                 ('D', 'Unità  da diporto'),
                                 ('E', 'Aeromobii')),
                                'Leasing')
    numero_operazioni_attive_aggregate = fields.Integer('Nr op. attive',
                                                        size=16)
    numero_operazioni_passive_aggregate = fields.Integer('Nr op. passive',
                                                         size=16)
    attive_imponibile_non_esente = fields.Float(
        'Tot impon., non impon ed esenti', digits=dp.get_precision('Account'),
        help="Totale operazioni imponibili, non imponibili ed esenti")
    attive_imposta = fields.Float(' Tot imposta',
                                  digits=dp.get_precision('Account'),
                                  help="Totale imposta")
    attive_operazioni_iva_non_esposta = fields.Float(
        'Totale operaz. IVA non esposta', digits=dp.get_precision('Account'),
        help="Totale operazioni con IVA non esposta")
    attive_note_variazione = fields.Float('Totale note variazione',
                                          digits=dp.get_precision('Account'),
                                          help="Totale note di variazione a debito per la controparte")
    attive_note_variazione_imposta = fields.Float(
        'Totale imposta note variazione', digits=dp.get_precision('Account'),
        help="Totale imposta sulle note di variazione a debito")

    passive_imponibile_non_esente = fields.Float(
        'Tot impon., non impon ed esenti', digits=dp.get_precision('Account'),
        help="Totale operazioni imponibili, non imponibili ed esenti")
    passive_imposta = fields.Float('Totale imposta',
                                   digits=dp.get_precision('Account'), help="Totale imposta")
    passive_operazioni_iva_non_esposta = fields.Float(
        'Totale operaz. IVA non esposta', digits=dp.get_precision('Account'),
        help="Totale operazioni con IVA non esposta")
    passive_note_variazione = fields.Float('Totale note variazione',
                                           digits=dp.get_precision('Account'),
                                           help="Totale note di variazione a credito per la controparte")
    passive_note_variazione_imposta = fields.Float(
        'Totale imposta note variazione', digits=dp.get_precision('Account'),
        help="Totale imposta sulle note di variazione a credito")

    @api.model
    def add_line(self, move, invoice, arg):
        # Partner
        if 'partner' in arg and arg['partner']:
            partner = arg['partner']
        else:
            partner = move.partner_id
        # Comunicazione
        comunicazione_id = arg.get('comunicazione_id', False)
        domain = [('comunicazione_id', '=', comunicazione_id),
                  ('partner_id', '=', partner.id)]
        com_line = self.search(domain)
        val_head = {}
        val = {}
        # Valori documento
        doc_vals = self.comunicazione_id.compute_amounts(move, invoice, arg)
        if not com_line:
            partita_iva = ''
            if partner.vat:
                partita_iva = partner.vat[2:]
            documento_riepilogativo = False
            if arg['operazione'] == 'DR':
                documento_riepilogativo = True
            val_head = {
                'comunicazione_id': comunicazione_id,
                'partner_id': partner.id,
                'partita_iva': partita_iva,
                'codice_fiscale': partner.fiscalcode or '',
                'noleggio': partner.spesometro_leasing or '',
                'documento_riepilogativo': documento_riepilogativo,
            }
        # Valori
        amount_untaxed = doc_vals.get('amount_untaxed', 0)
        amount_tax = doc_vals.get('amount_tax', 0)
        amount_total = doc_vals.get('amount_total', 0)
        # attive
        if arg.get('segno', False) == 'attiva':
            val['numero_operazioni_attive_aggregate'] = \
                com_line and (com_line.numero_operazioni_attive_aggregate + 1) \
                or 1
            if 'refund' in move.journal_id.type:
                val['attive_note_variazione'] = \
                    com_line and (com_line.attive_note_variazione +
                                  amount_untaxed) \
                    or amount_untaxed
                val['attive_note_variazione_imposta'] = \
                    com_line and (com_line.attive_note_variazione_imposta +
                                  amount_tax) \
                    or amount_tax
            else:
                if arg.get('operazione_iva_non_esposta', False):
                    val['attive_operazioni_iva_non_esposta' ] = \
                        com_line and (
                            com_line.attive_operazioni_iva_non_esposta +
                            amount_total) \
                        or amount_total
                else:
                    val['attive_imponibile_non_esente' ] = \
                        com_line and (com_line.attive_imponibile_non_esente +
                                      amount_untaxed) \
                        or amount_untaxed
                    val['attive_imposta'] = \
                        com_line and (com_line.attive_imposta + amount_tax) \
                        or amount_tax
        # passive
        else:
            val['numero_operazioni_passive_aggregate'] = \
                com_line and (com_line.numero_operazioni_passive_aggregate + 1)\
                or 1
            if 'refund' in move.journal_id.type:
                val['passive_note_variazione'] = \
                    com_line and (com_line.passive_note_variazione +
                                  amount_untaxed) \
                    or amount_untaxed
                val['passive_note_variazione_imposta'] = \
                    com_line and (com_line.passive_note_variazione_imposta +
                                  amount_tax) \
                    or amount_tax
            else:
                if arg.get('operazione_iva_non_esposta', False):
                    val['passive_operazioni_iva_non_esposta' ] = \
                        com_line and (
                            com_line.passive_operazioni_iva_non_esposta +
                            amount_total) \
                        or amount_total
                else:
                    val['passive_imponibile_non_esente' ] = \
                        com_line and (com_line.passive_imponibile_non_esente +
                                      amount_untaxed) \
                        or amount_untaxed
                    val['passive_imposta' ] = \
                        com_line and (com_line.passive_imposta + amount_tax) \
                        or amount_tax
        if com_line:
            return com_line.write(val)
        else:
            val.update(val_head)
            return self.create(val)


class spesometro_comunicazione_line_SA(models.Model):
    '''
    QUADRO SA - Operazioni senza fattura esposte in forma aggregata
    '''
    _name = "spesometro.comunicazione.line.sa"
    _description = "Spesometro - Comunicazione linee quadro SA"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione',
                                       ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner')
    codice_fiscale = fields.Char('Codice Fiscale', size=16)

    numero_operazioni = fields.Integer('Numero operazioni')
    importo_complessivo = fields.Float('Importo complessivo',
                                       digits=dp.get_precision('Account'))
    noleggio = fields.Selection((('A', 'Autovettura'),
                                 ('B', 'Caravan'),
                                 ('C', 'Altri Veicoli'),
                                 ('D', 'Unità  da diporto'),
                                 ('E', 'Aeromobii')),
                                'Leasing')

    @api.model
    def add_line(self, move, invoice, arg):
        # Partner
        if 'partner' in arg and arg['partner']:
            partner = arg['partner']
        else:
            partner = move.partner_id
        # Comunicazione
        comunicazione_id = arg.get('comunicazione_id', False)
        domain = [('comunicazione_id', '=', comunicazione_id),
                  ('partner_id', '=', partner.id)]
        com_line = self.search(domain)
        val_head = {}
        val = {}
        # Valori documento
        doc_vals = self.comunicazione_id.compute_amounts(move, invoice, arg)
        # New partner
        if not com_line:
            val_head = {
                'comunicazione_id': comunicazione_id,
                'partner_id': partner.id,
                'codice_fiscale': partner.fiscalcode or False,
                'noleggio': partner.spesometro_leasing or False,
            }
        # Valori
        amount_untaxed = doc_vals.get('amount_untaxed', 0)
        amount_tax = doc_vals.get('amount_tax', 0)
        amount_total = doc_vals.get('amount_total', 0)

        val['numero_operazioni'] = \
            com_line and (com_line.numero_operazioni + 1) or 1
        val['importo_complessivo'] = \
            com_line and (com_line.importo_complessivo + amount_total) \
            or amount_total

        if com_line:
            return com_line.write(val)
        else:
            val.update(val_head)
            return self.create(val)


class spesometro_comunicazione_line_BL(models.Model):
    '''
    QUADRO BL
    - Operazioni con paesi con fiscalità privilegiata (è obbligatorio compilare
        le sezioni BL001, BL002  e almeno un campo delle sezioni 
        BL003, BL004, BL005, BL006, BL007, BL008)
    - Operazioni con soggetti non residenti (è obbligatorio compilare le 
        sezioni BL001, BL002 e almeno un campo delle sezioni BL003 e BL006)
    - Acquisti di servizi da soggetti non residenti (è obbligatorio compilare 
        le sezioni BL001, BL002 e almeno un campo della sezione BL006)
    '''
    _name = "spesometro.comunicazione.line.bl"
    _description = "Spesometro - Comunicazione linee quadro BL"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione',
                                       ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner')
    codice_fiscale = fields.Char('Codice Fiscale', size=16)

    numero_operazioni = fields.Integer('Numero operazioni')
    importo_complessivo = fields.Integer('Importo complessivo',
                                         digits=dp.get_precision('Account'))
    noleggio = fields.Selection((('A', 'Autovettura'),
                                 ('B', 'Caravan'),
                                 ('C', 'Altri Veicoli'),
                                 ('D', 'Unità da diporto'),
                                 ('E', 'Aeromobii')),
                                'Leasing')

    pf_cognome = fields.Char('Cognome', size=24, help="")
    pf_nome = fields.Char('Nome', size=20, help="")
    pf_data_nascita = fields.Date('Data di nascita')
    pf_comune_stato_nascita = fields.Char('Comune o stato estero di nascita',
                                          size=40)
    pf_provincia_nascita = fields.Char('Provincia', size=2)
    pf_codice_stato_estero = fields.Char('Codice Stato Estero', size=3,
                                         help="Deve essere uno di quelli presenti nella tabella 'elenco dei \
        paesi e territori esteri' pubblicata nelle istruzioni del modello \
        Unico")
    pg_denominazione = fields.Char('Denominazione/Ragione sociale', size=60)
    pg_citta_estera_sede_legale = fields.Char('Città estera delle Sede legale',
                                              size=40)
    pg_codice_stato_estero = fields.Char('Codice Stato Estero', size=3,
                                         help="Deve essere uno di quelli presenti nella tabella\
        'elenco dei paesi e territori esteri' pubblicata nelle istruzioni del \
        modello Unico")
    pg_indirizzo_sede_legale = fields.Char('Indirizzo sede legale', size=60)

    codice_identificativo_IVA = fields.Char('Codice identificativo IVA',
                                            size=16)
    operazione_fiscalita_privilegiata = fields.Boolean(
        'Operazione con pesei con fiscalità privilegiata')
    operazione_con_soggetti_non_residenti = fields.Boolean(
        'Operazione con soggetto non residente')
    acquisto_servizi_da_soggetti_non_residenti = fields.Boolean('Acquisto \
        di servizi da soggetti non residenti')
    operazione_tipo_importo = fields.Selection((
        ('INE', 'Imponibile, Non Imponibile, Esente'),
        ('NS', 'Non Soggette ad IVA'),
        ('NV', 'Note di variazione')),
        'Tipo Importo')

    attive_importo_complessivo = fields.Float(
        'Tot operaz. attive impon., non impon ed esenti',
        digits=dp.get_precision('Account'),
        help="Totale operazioni imponibili, non imponibili ed esenti")
    attive_imposta = fields.Float('Tot operaz. attive imposta',
                                  digits=dp.get_precision('Account'),
                                  help="Totale imposta")
    attive_non_sogg_cessione_beni = fields.Float(
        'Operaz.attive non soggette ad IVA - Cessione beni',
        digits=dp.get_precision('Account'),
        help="Totale operazioni imponibili, non imponibili ed esenti")
    attive_non_sogg_servizi = fields.Float(
        'Operaz.attive non soggette ad IVA - Servizi',
        digits=dp.get_precision('Account'),
        help="Totale operazioni imponibili, non imponibili ed esenti")
    attive_note_variazione = fields.Float('Totale note variazione',
                                          digits=dp.get_precision('Account'),
                                          help="Totale note di variazione a debito per la controparte")
    attive_note_variazione_imposta = fields.Float(
        'Totale imposta note variazione',
        digits=dp.get_precision('Account'),
        help="Totale imposta sulle note di variazione a debito")

    passive_importo_complessivo = fields.Float(
        'Tot operaz. passive impon., non impon ed esenti',
        digits=dp.get_precision('Account'),
        help="Totale operazioni imponibili, non imponibili ed esenti")
    passive_imposta = fields.Float(
        'Tot operaz. passive imposta',
        digits=dp.get_precision('Account'),
        help="Totale imposta")
    passive_non_sogg_importo_complessivo = fields.Float(
        'Operaz.passive non soggette ad IVA',
        digits=dp.get_precision('Account'),
        help="Totale operazioni imponibili, non imponibili ed esenti")
    passive_note_variazione = fields.Float(
        'Totale note variazione',
        digits=dp.get_precision('Account'),
        help="Totale note di variazione a debito per la controparte")
    passive_note_variazione_imposta = fields.Float(
        'Totale imposta note variazione',
        digits=dp.get_precision('Account'),
        help="Totale imposta sulle note di variazione a debito")

    @api.model
    def add_line(self, move, invoice, arg):
        # Partner
        if 'partner' in arg and arg['partner']:
            partner = arg['partner']
        else:
            partner = move.partner_id
        # Operazione
        operazione = arg.get('operazione')
        # Operazione tipo importo
        operazione_tipo_importo = arg.get('operazione_tipo_importo')
        # Tipo servizio
        tipo_servizio = arg.get('tipo_servizio')
        # Comunicazione
        comunicazione_id = arg.get('comunicazione_id', False)
        domain = [('comunicazione_id', '=', comunicazione_id),
                  ('partner_id', '=', partner.id)]
        com_line = self.search(domain)
        val_head = {}
        val = {}
        # Valori documento
        doc_vals = self.comunicazione_id.compute_amounts(move, invoice, arg)
        amount_untaxed = doc_vals.get('amount_untaxed', 0)
        amount_tax = doc_vals.get('amount_tax', 0)
        amount_total = doc_vals.get('amount_total', 0)
        # Head
        if not com_line:
            # p.iva
            if partner.vat:
                partita_iva = partner.vat[2:]
            else:
                partita_iva = '{:11s}'.format("".zfill(11))
            # prov. nascita
            prov_code = False
            val_head = {
                'comunicazione_id': comunicazione_id,
                'partner_id': partner.id,
                'codice_fiscale': partner.fiscalcode or False,
                'codice_identificativo_IVA': partner.vat or False,
                'noleggio': partner.spesometro_leasing or False,
                'operazione_tipo_importo': operazione_tipo_importo or False,

                'pg_denominazione': partner.name or False,
                'pg_citta_estera_sede_legale': partner.city or False,
                'pg_codice_stato_estero':
                partner.country_id.codice_stato_agenzia_entrate or '',
                'pg_indirizzo_sede_legale': partner.street or False,

                'operazione_fiscalita_privilegiata': False,
                'operazione_con_soggetti_non_residenti': False,
                'acquisto_servizi_da_soggetti_non_residenti': False,
            }
            if operazione == 'BL1':
                val_head['operazione_fiscalita_privilegiata'] = True
            elif operazione == 'BL2':
                val_head['operazione_con_soggetti_non_residenti'] = True
            elif operazione == 'BL3':
                val_head['acquisto_servizi_da_soggetti_non_residenti'] = True
        # Amounts
        # ...attive
        if arg.get('segno', False) == 'attiva':

            # BL003 - Operazioni imponibili, non imponibili ed esenti
            if operazione_tipo_importo == 'INE':
                val['attive_importo_complessivo'] = com_line and \
                    (com_line.attive_importo_complessivo + amount_total) \
                    or amount_total
                val['attive_imposta'] = com_line and \
                    (com_line.attive_imposta + amount_tax) or amount_tax
            # BL004 - Operazioni non soggette ad IVA
            elif operazione_tipo_importo == 'NS':
                if tipo_servizio == 'cessioni':
                    val['attive_non_sogg_cessione_beni'] = com_line and \
                        (com_line.attive_non_sogg_cessione_beni + amount_total)\
                        or amount_total
                else:
                    val['attive_non_sogg_servizi'] = com_line and \
                        (com_line.attive_non_sogg_servizi + amount_total)\
                        or amount_total
            # BL005 - Note di variazione
            elif operazione_tipo_importo == 'NV':
                val['attive_note_variazione'] = com_line and \
                    (com_line.attive_note_variazione + amount_untaxed) \
                    or amount_untaxed
                val['attive_note_variazione_imposta'] = com_line and \
                    (com_line.attive_note_variazione_imposta + amount_tax) \
                    or amount_tax
        # ...passive
        else:
            # BL006 - Operazioni imponibili, non imponibili ed esenti
            if operazione_tipo_importo == 'INE':
                val['passive_importo_complessivo'] = com_line and \
                    (com_line.passive_importo_complessivo + amount_total) \
                    or amount_total
                val['passive_imposta'] = com_line and \
                    (com_line.passive_imposta + amount_tax) or amount_tax
            # BL007 - Operazioni non soggette ad IVA
            elif operazione_tipo_importo == 'NS':
                val['passive_non_sogg_importo_complessivo'] = com_line and \
                    (com_line.passive_non_sogg_importo_complessivo +
                     amount_total) or amount_total
            # BL008 - Note di variazione
            elif operazione_tipo_importo == 'NV':
                val['passive_note_variazione'] = com_line and \
                    (com_line.passive_note_variazione + amount_untaxed) \
                    or amount_untaxed
                val['passive_note_variazione_imposta'] = com_line and \
                    (com_line.passive_note_variazione_imposta + amount_tax) \
                    or amount_tax

        if com_line:
            return com_line.write(val)
        else:
            val.update(val_head)
            return self.create(val)


class spesometro_comunicazione_line_FE(models.Model):

    _name = "spesometro.comunicazione.line.fe"
    _description = "Spesometro - Comunicazione linee quadro FE"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione', ondelete='cascade')

    partner_id = fields.Many2one('res.partner', 'Partner')
    partita_iva = fields.Char('Partita IVA', size=11)
    codice_fiscale = fields.Char('Codice Fiscale', size=16)
    documento_riepilogativo = fields.Boolean('Documento Riepilogativo')
    noleggio = fields.Selection((('A', 'Autovettura'),
                                 ('B', 'Caravan'),
                                 ('C', 'Altri Veicoli'),
                                 ('D', 'Unità  da diporto'),
                                 ('E', 'Aeromobii')),
                                'Leasing')

    autofattura = fields.Boolean('Autofattura')
    data_documento = fields.Date('Data documento')
    data_registrazione = fields.Date('Data registrazione')
    numero_fattura = fields.Char('Numero Fattura - Doc riepilog.', size=16)

    importo = fields.Float('Importo', digits=dp.get_precision('Account'))
    imposta = fields.Float('Imposta', digits=dp.get_precision('Account'))


class spesometro_comunicazione_line_FR(models.Model):

    _name = "spesometro.comunicazione.line.fr"
    _description = "Spesometro - Comunicazione linee quadro FR"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione', ondelete='cascade')

    partner_id = fields.Many2one('res.partner', 'Partner')
    partita_iva = fields.Char('Partita IVA', size=11)
    documento_riepilogativo = fields.Boolean('Documento Riepilogativo')
    data_documento = fields.Date('Data documento')
    data_registrazione = fields.Date('Data registrazione')
    iva_non_esposta = fields.Boolean('IVA non esposta')
    reverse_charge = fields.Boolean('Reverse charge')
    autofattura = fields.Boolean('Autofattura')

    importo = fields.Float('Importo', digits=dp.get_precision('Account'))
    imposta = fields.Float('Imposta', digits=dp.get_precision('Account'))


class spesometro_comunicazione_line_NE(models.Model):

    _name = "spesometro.comunicazione.line.ne"
    _description = "Spesometro - Comunicazione linee quadro NE"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione',
                                       ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner')
    partita_iva = fields.Char('Partita IVA', size=11)
    codice_fiscale = fields.Char('Codice Fiscale', size=16)
    data_emissione = fields.Date('Data emissione')
    data_registrazione = fields.Date('Data registrazione')
    numero_nota = fields.Char('Numero Nota', size=16)

    importo = fields.Float('Importo', digits=dp.get_precision('Account'))
    imposta = fields.Float('Imposta', digits=dp.get_precision('Account'))


class spesometro_comunicazione_line_NR(models.Model):

    _name = "spesometro.comunicazione.line.nr"
    _description = "Spesometro - Comunicazione linee quadro NR"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione',
                                       ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner')
    partita_iva = fields.Char('Partita IVA', size=11)
    data_documento = fields.Date('Data documento')
    data_registrazione = fields.Date('Data registrazione')

    importo = fields.Float('Importo', digits=dp.get_precision('Account'))
    imposta = fields.Float('Imposta', digits=dp.get_precision('Account'))


class spesometro_comunicazione_line_DF(models.Model):

    _name = "spesometro.comunicazione.line.df"
    _description = "Spesometro - Comunicazione linee quadro DF"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione',
                                       ondelete='cascade')

    partner_id = fields.Many2one('res.partner', 'Partner')
    codice_fiscale = fields.Char('Codice Fiscale', size=16)
    data_operazione = fields.Date('Data operazione')

    importo = fields.Float('Importo', digits=dp.get_precision('Account'))
    noleggio = fields.Selection((('A', 'Autovettura'),
                                 ('B', 'Caravan'),
                                 ('C', 'Altri Veicoli'),
                                 ('D', 'Unità  da diporto'),
                                 ('E', 'Aeromobii')),
                                'Leasing')


class spesometro_comunicazione_line_FN(models.Model):

    _name = "spesometro.comunicazione.line.fn"
    _description = "Spesometro - Comunicazione linee quadro FN"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione',
                                       ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner')

    pf_cognome = fields.Char('Cognome', size=24, help="")
    pf_nome = fields.Char('Nome', size=20, help="")
    pf_data_nascita = fields.Date('Data di nascita')
    pf_comune_stato_nascita = fields.Char('Comune o stato estero di nascita',
                                          size=40)
    pf_provincia_nascita = fields.Char('Provincia', size=2)
    pf_codice_stato_estero_domicilio = fields.Char(
        'Codice Stato Estero del Domicilio', size=3,
        help="Deve essere uno di quelli presenti nella tabella 'elenco dei \
            paesi e territori esteri' pubblicata nelle istruzioni del \
            modello Unico")

    pg_denominazione = fields.Char('Denominazione/Ragione sociale', size=60)
    pg_citta_estera_sede_legale = fields.Char('Città estera delle Sede legale',
                                              size=40)
    pg_codice_stato_estero_domicilio = fields.Char(
        'Codice Stato Estero del Domicilio', size=3,
        help="Deve essere uno di quelli presenti nella tabella 'elenco dei \
            paesi e territori esteri' pubblicata nelle istruzioni del modello \
            Unico")
    pg_indirizzo_sede_legale = fields.Char('Indirizzo legale', size=40)

    data_emissione = fields.Date('Data emissione')
    data_registrazione = fields.Date('Data registrazione')
    numero_fattura = fields.Char('Numero Fattura/Doc riepilog.', size=16)
    noleggio = fields.Selection((('A', 'Autovettura'),
                                 ('B', 'Caravan'),
                                 ('C', 'Altri Veicoli'),
                                 ('D', 'Unità  da diporto'),
                                 ('E', 'Aeromobii')),
                                'Leasing')
    importo = fields.Float('Importo', digits=dp.get_precision('Account'))
    imposta = fields.Float('Imposta', digits=dp.get_precision('Account'))


class spesometro_comunicazione_line_SE(models.Model):
    '''
    QUADRO SE - Acquisti di servizi da non residenti e Acquisti da operatori di 
    San Marino
    '''
    _name = "spesometro.comunicazione.line.se"
    _description = "Spesometro - Comunicazione linee quadro SE"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione',
                                       ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner')

    pf_cognome = fields.Char('Cognome', size=24, help="")
    pf_nome = fields.Char('Nome', size=20, help="")
    pf_data_nascita = fields.Date('Data di nascita')
    pf_comune_stato_nascita = fields.Char('Comune o stato estero di nascita',
                                          size=40)
    pf_provincia_nascita = fields.Char('Provincia', size=2)
    pf_codice_stato_estero_domicilio = fields.Char(
        'Codice Stato Estero del Domicilio', size=3,
        help="Deve essere uno di quelli presenti nella tabella 'elenco dei \
            paesi e territori esteri' pubblicata nelle istruzioni del modello \
            Unico")

    pg_denominazione = fields.Char('Denominazione/Ragione sociale', size=60)
    pg_citta_estera_sede_legale = fields.Char('Città estera delle Sede legale',
                                              size=40)
    pg_codice_stato_estero_domicilio = fields.Char(
        'Codice Stato Estero del Domicilio', size=3,
        help="Deve essere uno di quelli presenti nella tabella 'elenco dei \
            paesi e territori esteri' pubblicata nelle istruzioni del modello \
            Unico")
    pg_indirizzo_sede_legale = fields.Char('Indirizzo legale', size=40)

    codice_identificativo_IVA = fields.Char(
        'Codice Identificativo IVA (037=San Marino)', size=3)
    data_emissione = fields.Date('Data emissione')
    data_registrazione = fields.Date('Data registrazione')
    numero_fattura = fields.Char('Numero Fattura/Doc riepilog.', size=16)

    importo = fields.Float('Importo/imponibile',
                           digits=dp.get_precision('Account'))
    imposta = fields.Float('Imposta', digits=dp.get_precision('Account'))

    @api.model
    def add_line(self, move, invoice, arg):
        # Partner
        if 'partner' in arg and arg['partner']:
            partner = arg['partner']
        else:
            partner = move.partner_id
        # Comunicazione
        comunicazione_id = arg.get('comunicazione_id', False)
        domain = [('comunicazione_id', '=', comunicazione_id),
                  ('partner_id', '=', partner.id)]
        com_line = self.search(domain)
        val_head = {}
        val = {}
        # Valori documento
        doc_vals = self.comunicazione_id.compute_amounts(move, invoice, arg)

        # p.iva
        if partner.vat:
            partita_iva = partner.vat[2:]
        else:
            partita_iva = '{:11s}'.format("".zfill(11))

        # Indirizzo
        address = self.env['spesometro.comunicazione'].\
            _get_partner_address_obj(move, invoice, arg)
        # Codice identificativo IVA -Da indicare esclusivamente per operazioni\
        #     con San Marino (Codice Stato = 037)
        codice_identificativo_iva = ''
        if self.env['spesometro.comunicazione'].partner_is_from_san_marino(
                move, invoice, arg):
            codice_identificativo_iva = '037'
        val = {
            'comunicazione_id': comunicazione_id,
            'partner_id': partner.id,
            'codice_fiscale': partner.fiscalcode or False,
            'noleggio': partner.spesometro_leasing or False,

            'pg_denominazione': partner.name or False,
            'pg_citta_estera_sede_legale': address.city or False,
            'pg_codice_stato_estero_domicilio':
            address.country_id.codice_stato_agenzia_entrate or
            codice_identificativo_iva or '',
            'pg_indirizzo_sede_legale': address.street or False,

            'codice_identificativo_IVA': codice_identificativo_iva,

            'data_emissione': move.date,
            'data_registrazione': invoice.date_invoice or move.date,
            'numero_fattura': move.name,

            'importo': doc_vals.get('amount_untaxed', 0),
            'imposta': doc_vals.get('amount_tax', 0)
        }

        return self.create(val)


class spesometro_comunicazione_line_TU(models.Model):

    _name = "spesometro.comunicazione.line.tu"
    _description = "Spesometro - Comunicazione linee quadro TU"

    comunicazione_id = fields.Many2one('spesometro.comunicazione',
                                       'Comunicazione',
                                       ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner')

    cognome = fields.Char('Cognome', size=24, help="")
    nome = fields.Char('Nome', size=20, help="")
    data_nascita = fields.Date('Data di nascita')
    comune_stato_nascita = fields.Char('Comune o stato estero di nascita',
                                       size=40)
    provincia_nascita = fields.Char('Provincia', size=2)
    citta_estera_residenza = fields.Char('Città Estera di residenza',
                                         size=40)
    codice_stato_estero = fields.Char('Codice Stato Estero', size=3,
                                      help="Deve essere uno di quelli presenti nella tabella 'elenco dei \
            paesi e territori esteri' pubblicata nelle istruzioni del modello \
            Unico")
    indirizzo_estero_residenza = fields.Char('Indirizzo Estero di residenza',
                                             size=40)
    data_emissione = fields.Date('Data emissione')
    data_registrazione = fields.Date('Data registrazione')
    numero_fattura = fields.Char('Numero Fattura/Doc riepilog.', size=16)

    importo = fields.Float('Importo/imponibile',
                           digits=dp.get_precision('Account'))
    imposta = fields.Float('Imposta', digits=dp.get_precision('Account'))
