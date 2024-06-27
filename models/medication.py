# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Medication(models.Model):
    _name = "medication"
    _description = "Medication"
    _rec_name = "ref"

    name = fields.Char(string='Name')
    ref = fields.Char(string='Reference', readonly=True)
    price = fields.Float(string='Price')
    description = fields.Text(string='Description')

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('medication')
        return super(Medication, self).create(vals)
