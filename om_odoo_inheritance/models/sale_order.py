# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    confirmed_user_id = fields.Many2one(comodel_name='res.users', string='Confirmed User')
    page_ids = fields.One2many('sale.order.page', 'sale_id', string='Page')
    percent = fields.Integer(string='Percent', required=True)
    profit = fields.Float(string='Profit', compute='_compute_profit', readonly=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True, readonly=True)

    @api.model
    def action_confirm(self):  # if is fund parameter write def action_confirm(self, para1, para2, ...)
        self.confirmed_user_id = self.env.user  # (self.env.user) get the user using the server
        super(SaleOrder, self).action_confirm()  # action_confirm(self, para1, para2, ...)
        # self.confirmed_user_id = self.env.user.id # (self.env.user.id) get the user using the server and you con

    @api.constrains('percent')
    def _check_percent(self):
        for rec in self:
            if rec.percent < 0 or rec.percent > 100:
                raise ValidationError(_("The percent should be between 0 and 100."))

    @api.depends('percent', 'total')
    def _compute_profit(self):
        for rec in self:
            rec.profit = (rec.percent / 100) * rec.total

    @api.depends('page_ids')
    def _compute_total(self):
        total = 0.0
        for rec in self.page_ids:
            total += rec.amount

        self.total = total

class SaleOrderPage(models.Model):
    _name = "sale.order.page"
    _description = "Sale Order Page"

    sale_id = fields.Many2one('sale.order', string='Sale')
    amount = fields.Float(string='Amount')
    date = fields.Date(string='Date')
    currency_id = fields.Many2one('res.currency', string='Currency')

