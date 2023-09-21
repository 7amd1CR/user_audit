# -*- coding: utf-8 -*-
from odoo import models, fields, api




class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    crm_send_email_action_before = fields.Integer(related='company_id.crm_send_email_action_before', readonly=False)
    purchase_send_email_action_before = fields.Integer(related='company_id.purchase_send_email_action_before', readonly=False)
    employee_send_email_action_before = fields.Integer(related='company_id.employee_send_email_action_before', readonly=False)



class ResCompany(models.Model):
    _inherit = "res.company"

    crm_send_email_action_before = fields.Integer()
    purchase_send_email_action_before = fields.Integer()
    employee_send_email_action_before = fields.Integer()