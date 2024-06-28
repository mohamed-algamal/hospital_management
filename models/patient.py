# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = "patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Patient"
    _order = 'id desc'

    name = fields.Char(string='Name')
    ref = fields.Char(string='Reference', readonly=True)
    date_of_birth = fields.Date(string='Date Of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='gender')
    image = fields.Image(string='Image')
    # patient_ = fields.Many2one('hospital.appointment', string='appointment')
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('appointment', 'patient_id', string='Appointment')
    operation_count = fields.Integer(string='Operation Count', compute='_compute_operation_count', store=True)
    operation_ids = fields.One2many('operation', 'patient_id', string='Operation')
    doctor_ids = fields.Many2many(comodel_name='res.users', string='Doctors', tracking=True)
    parent = fields.Char(string='Parent')
    partner_name = fields.Char(string='Partner Name')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('other', 'Other'),
    ], string='Marital Status')
    operation_id = fields.Many2one('operation', string='Operation')
    is_birthday = fields.Boolean(string='Is Birthday ?', compute='_compute_is_birthday')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    def action_view_appointments(self):
        return {  # button box
            'name': _('Appointments'),  # any name you want
            'res_model': 'appointment',  # the name model have the views
            'view_mode': 'tree,form',  # any view you want show
            'context': {
                'patient_id': self.id
            },  # enter the default value
            'domain': [('patient_id', '=', self.id)],  # set the condition
            'target': 'current',  # current and new and inline
            'type': 'ir.actions.act_window',
        }

    def action_view_operation(self):
        return {  # button box
            'name': _('Operation'),  # any name you want
            'res_model': 'operation',  # the name model have the views
            'view_mode': 'tree,form',  # any view you want show
            'context': {
                'patient_id': self.id
            },  # enter the default value
            'domain': [('patient_id', '=', self.id)],  # set the condition
            'target': 'current',  # current and new and inline
            'type': 'ir.actions.act_window',
        }
    
    @api.depends('operation_ids')
    def _compute_operation_count(self):  # stored computed field
        # operation_group = self.env['operation'].read_group(domain=[], fields=['patient_id'], groupby=['patient_id'])
        # # print("appointment_group > ", appointment_group)
        # for operation in operation_group:
        #     # print("appointment > ", appointment)
        #     patient_id = operation.get('patient_id')[0]
        #     # print("patient_id > ", patient_id)
        #     patient_rec = self.browse(patient_id)
        #     # print("patient_rec > ", patient_rec)
        #     patient_rec.operation_count = operation['patient_id_count']
        #     self -= patient_rec
        # self.operation_count = 0
        count = self.env['operation'].search_count([('patient_id', '=', self.id)])
        self.operation_count = count


    @api.depends('appointment_ids')
    def _compute_appointment_count(self):  # stored computed field
        # appointment_group = self.env['appointment'].read_group(domain=[], fields=['patient_id'],
        #                                                        groupby=['patient_id'])
        # print("appointment_group > ", appointment_group)
        # for appointment in appointment_group:
        #     print("appointment > ", appointment)
        #     patient_id = appointment.get('patient_id')[0]
        #     print("patient_id > ", patient_id)
        #     patient_rec = self.browse(patient_id)
        #     print("patient_rec > ", patient_rec)
        #     patient_rec.appointment_count = appointment['patient_id_count']
        #     self -= patient_rec
        # self.appointment_count = 0
        count = self.env['appointment'].search_count([('patient_id', '=', self.id )])
        self.appointment_count = count
        
    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            rec.is_birthday = False
            if rec.date_of_birth:
                if date.today().day == rec.date_of_birth.day and date.today().month == rec.date_of_birth.month:
                    rec.is_birthday = True

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('patient')
        return super(Patient, self).create(vals)

