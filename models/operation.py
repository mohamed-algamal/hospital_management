# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Operation(models.Model):
    _name = "operation"
    _description = "Operation"
    _log_access = False
    _order = 'id desc'
    _rec_name = 'ref'

    name = fields.Char(string='Name', required=True)
    ref = fields.Char(string='Reference', readonly=True)
    patient_id = fields.Many2one('patient', string='Patient',required=True)
    doctor_ids = fields.Many2many('res.users', 'doctor_operation_rel', 'doctor', 'users', string='Doctor')
    nurse_ids = fields.Many2many('res.users', 'nurse_operation_rel', 'nurse', 'users', string='Nurse')
    description = fields.Html(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('prepare', 'Prepare'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft', string='Status', required=True)
    check_done = fields.Boolean()
    check_cancel = fields.Boolean()

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('operation')
        return super(Operation, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):  # ref is empty
            vals['ref'] = self.env['ir.sequence'].next_by_code('patient')
        return super(Operation, self).write(vals)

    def action_prepare(self):
        for rec in self:
            rec.state = 'prepare'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            rec.check_done = True

