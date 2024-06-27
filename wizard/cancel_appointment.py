# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['data_cancel'] = date.today()
        if self.env.context.get('active_id'):
            record = self.env['appointment'].browse(self.env.context.get('active_id'))
            res['appointment_id'] = record
            res['patient'] = record.patient_id.name
            # res['patient'] = self.env.context.get('uid')
            res['user_id'] = self.env.user.id
        return res

    appointment_id = fields.Many2one('appointment', string='Appointment', readonly=True)
    patient = fields.Char(string='Patient', readonly=True)
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    reason = fields.Text(string='Reason', required=True)
    data_cancel = fields.Date(string='Cancel Date', readonly=True)

    def action_cancel(self):
        print("algamal")
        pass

    # def action_cancel(self):
        # cancel_day = self.env['ir.config_parameter'].sudo().get_param('om_hospital.cancel_days')  # return string value
        # days = (date.today() - self.apporintent_id.booking_date).days
        # if self.apporintent_id.booking_date == fields.Date.today():
        #     raise ValidationError(_("Sorry, cancellation is not allowed on the same day of booking !"))
        # if int(cancel_day) != 0 and days <= int(cancel_day):
        #     self.apporintent_id.state = 'cancel'
        # else:
        #     raise ValidationError(_("you can't cancellation this appointment"))

        # query = """select id,name from hospital_patient"""
        # query = f"""select id,patient_id from hospital_apporintent where id = {self.apporintent_id.id}"""
        # self.env.cr.execute("""select name form hospital_patient""")
        # self.env.cr.execute(query)
        # patient = self.env.cr.fetchall()  # return tuple enter list
        # patient = self.env.cr.dictfetchall()  # return dict enter list
        # patient = self.env.cr.dictfetchone()  # return one record
        # print("patient-------->", patient)

        # return {  # for don't prevent close the pop pu
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'cancel.apporintent.wizard',
        #     'target': 'new',
        #     'res_id': self.id,
        # }
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

        # pass



