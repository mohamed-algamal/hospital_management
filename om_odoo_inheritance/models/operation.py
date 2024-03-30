# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _inherit = ['hospital.operation', 'mail.thread', 'mail.activity.mixin']

    ref = fields.Char(tracking=True)
    doctor_id = fields.Many2one(tracking=True)
    operation_name = fields.Char(tracking=True)




