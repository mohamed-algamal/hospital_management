# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError


class CancelWizard(models.TransientModel):
    _name = 'cancel.wizard'
    _description = 'Cancel Wizard'

    @api.model
    def default_get(self, fields):
        res = super(CancelWizard, self).default_get(fields)
        res['data_cancel'] = date.today()

        if self.env.context.get('active_model') == 'appointment':
            record = self.env['appointment'].browse(self.env.context.get('active_id'))
            res['appointment_id'] = record.id
            res['patient'] = record.patient_id.name
            # res['user_id'] = self.env.context.get('uid')
            res['user_id'] = self.env.user.id
            return res
        elif self.env.context.get('active_model') == 'operation':
            record = self.env['operation'].browse(self.env.context.get('active_id'))
            res['operation_id'] = record.id
            res['patient'] = record.patient_id.name
            # res['user_id'] = self.env.context.get('uid')
            res['user_id'] = self.env.user.id
            return res

        return res

    appointment_id = fields.Many2one('appointment', string='Appointment', readonly=True)
    operation_id = fields.Many2one('operation', string='Operation', readonly=True)
    patient = fields.Char(string='Patient', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    reason = fields.Text(string='Reason', required=True)
    data_cancel = fields.Date(string='Cancel Date', readonly=True)

    def action_cancel(self):
        for rec in self:
            vals = {
                'patient': rec.patient,
                'user_id': rec.user_id.id,
                'reason': rec.reason,
                'data_cancel': rec.data_cancel,
            }
            if rec.appointment_id:
                rec.appointment_id.state = 'cancel'
                rec.appointment_id.check_cancel = True
                vals['name'] = f"{'Appointment'} ({rec.appointment_id.ref})"
                vals['type'] = 'appointment'
                rec.env['reason.cancel'].create(vals)
            else:
                rec.operation_id.state = 'cancel'
                rec.operation_id.check_cancel = True
                vals['name'] = f"{'Operation'} ({rec.operation_id.ref})"
                vals['type'] = 'operation'
                rec.env['reason.cancel'].create(vals)
