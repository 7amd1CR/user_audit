from odoo import fields, models, api
from datetime import datetime


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    email_user = fields.Many2one('res.users', copy=False)

    def check_activity(self):
        today = datetime.today().date()
        for order in self.search([]):
            msg_body = "Purchase Activity Notification  " + "<br/>"
            msg_body += "Please Check order %s  " % order.name + "<br/>"
            activities = self.env['mail.activity'].search(
                [('res_model', '=', 'purchase.order'), ('res_id', '=', order.id)])
            for activity in activities:
                if (
                        today - activity.date_deadline).days <= order.company_id.purchase_send_email_action_before and order.company_id.purchase_send_email_action_before:
                    email_user = activity.user_id
                    partner = email_user.partner_id
                    if partner:
                        partner.message_post(message_type='email', body=msg_body, partner_ids=[partner.id])
                    order_employee_parent_id = order.user_id.employee_parent_id
                    if order_employee_parent_id.user_id:
                        order.email_user = order_employee_parent_id.user_id.id
                else:
                    email_user = activity.user_id
                    partner = email_user.partner_id
                    if partner:
                        partner.message_post(message_type='email', body=msg_body, partner_ids=[partner.id])
                    order_employee_parent_id = order.email_user.employee_parent_id or order.user_id.employee_parent_id
                    if order_employee_parent_id.user_id:
                        order.email_user = order_employee_parent_id.user_id.id
