# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError


class ReasonCancelAppointment(models.Model):
    _name = 'reason.cancel.appointment'
    _description = 'Reason Cancel Appointment'

    appointment_id = fields.Many2one('appointment', string='Appointment', readonly=True)
    patient = fields.Char(string='Patient', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    reason = fields.Text(string='Reason', required=True)
    data_cancel = fields.Date(string='Cancel Date', readonly=True)



