# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


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
    # patient_ = fields.Many2one('hospital.apporintent', string='Apportinent')
    # appointment_count = fields.Integer(string='Appointment count', compute='_compute_appointment_count', store=True)
    # appointment_ids = fields.One2many('hospital.apporintent', 'patient_id', string='Appointment')
    # parent = fields.Char(string='Parent')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('other', 'Other'),  # Consider including this for flexibility
    ], string='Marital Status')
    partner_name = fields.Char(string='Partner Name')
    operation_id = fields.Many2one('hospital.operation', string='Operation')
    is_birthday = fields.Boolean(string='Is Birthday ?', compute='_compute_is_birthday')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    @api.depends('date_of_birth')  # because age depends date_of_birth when add value in date_of_birth
    def _compute_age(self):
        for rec in self:  # because don't make singleton error
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:  # you should add else in compute function
                rec.age = 0
