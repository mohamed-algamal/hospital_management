# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date


class Appointment(models.Model):
    _name = "appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Appointment"
    _rec_name = "ref"
    _order = 'id desc'

    patient_id = fields.Many2one(comodel_name='patient', string='Patient', tracking=1, required=True)
    gender = fields.Selection(related='patient_id.gender')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now, readonly=True)
    ref = fields.Char(string='Reference', readonly=True)
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string='Priority')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft', string='Status', required=True)
    doctor_id = fields.Many2one(comodel_name='res.users', string='Doctor', tracking=True, required=True)
    nurse_id = fields.Many2one(comodel_name='res.users', string='Nurse', tracking=True, required=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    progress = fields.Integer(string='Progress', compute='_compute_progress')
    check_done = fields.Boolean()
    check_cancel = fields.Boolean()
    # company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    # currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    def set_line_number(self):
        sl_no = 0
        for line in self.pharmacy_line_ids:
            sl_no += 1
            line.sl_no = sl_no

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('appointment')
        res = super(Appointment, self).create(vals)
        res.set_line_number()
        return res

    def write(self, vals):
        res = super(Appointment, self).write(vals)
        self.set_line_number()
        return res

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError(_("You can't delete done record!"))
        return super(Appointment, self).unlink()

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

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

    def action_cancel(self):
        for rec in self:
            rec.check_cansel = True
            action = rec.env.ref('hospital_management.action_cancel_appointment').read()[0]
            return action

    # def action_send_email(self):
    #     template = self.env.ref('om_hospital.appointment_mail_template')  # external id for email template
    #     for rec in self:
    #         if rec.patient_id.email:
    #             email_values = {'subject': 'Test OM'}
    #             template.send_mail(rec.id, force_send=True, email_values=email_values)  #force_send=True for send mail immediately

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = 25
            elif rec.state == 'in_consultation':
                progress = 50
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    sl_no = fields.Integer(string="SNO")
    medication_id = fields.Many2one('medication', required=True)
    price_unit = fields.Float(string='Price', digits='medication Price', compute='_compute_price_unit', store=True)
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('appointment', string='appointment')
    total_price = fields.Float(string='Total Price', compute='_compute_sum_price', store=True)

    @api.depends('price_unit', 'qty')
    def _compute_sum_price(self):
        for rec in self:
            rec.total_price = (rec.price_unit * rec.qty)

    @api.depends('medication_id')
    def _compute_price_unit(self):
        for rec in self:
            rec.price_unit = rec.medication_id.price
