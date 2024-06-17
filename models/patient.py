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
    # appointment_count = fields.Integer(string='Appointment count', compute='_compute_appointment_count', store=True)
    # appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointment')
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

