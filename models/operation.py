# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Operation(models.Model):
    _name = "operation"
    _description = "Operation"
    _log_access = False
    _order = 'id desc'
    _rec_name = 'ref'

    name = fields.Char(string='Name', required=True)
    ref = fields.Char(string='Reference', readonly=True)
    patient_id = fields.Many2one('patient', string='Patient', required=True)
    gender = fields.Char(compute='_compute_gender', readonly=True)
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
    check_send_email = fields.Boolean()

    def action_send_email(self):
        if self.check_send_email:
            raise ValidationError(_("Email already sent!"))
        template = self.env.ref('hospital_management.operation_mail_template')
        for rec in self:
            if rec.patient_id.email:
                rec.check_send_email = True
                template.send_mail(rec.id, force_send=True)
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': 'Email sent successfully',
                        'type': 'rainbow_man', }
                }

    @api.depends('patient_id')
    def _compute_gender(self):
        for rec in self:
            rec.gender = rec.patient_id.gender

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
            self.state = 'done'
            rec.check_done = True
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Done',
                    'type': 'rainbow_man',
                }
            }
