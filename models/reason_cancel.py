# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError


class ReasonCancel(models.Model):
    _name = 'reason.cancel'
    _description = 'Reason Cancel'

    name = fields.Char(string='Name')
    patient = fields.Char(string='Patient', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    reason = fields.Text(string='Reason', required=True)
    data_cancel = fields.Date(string='Cancel Date', readonly=True)
    type = fields.Selection([
        ('appointment', 'Appointment'),
        ('operation', 'Operation'), ], string='Type', readonly=True)

