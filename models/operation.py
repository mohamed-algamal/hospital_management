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

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('operation')
        return super(Operation, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):  # ref is empty
            vals['ref'] = self.env['ir.sequence'].next_by_code('patient')
        return super(Operation, self).write(vals)



    # @api.model
    # def name_create(self, name):  # create record from many2one field
    #     return self.create({'operation_name': name}).name_get()[0]
    #
    # def name_get(self):
    #     # patient_list = []
    #     # for rec in self:
    #     #     name = '[' + rec.ref + '] ' + rec.name
    #     #     patient_list.append((rec.id, name)) # (rec.id, name) this is tuple append in list
    #     # return patient_list
    #     return [(rec.id, f"[{rec.ref}] and {rec.operation_name}") for rec in self]  # return tuple enter list
