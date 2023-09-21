from odoo import fields, models, api
from datetime import datetime


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    email_user = fields.Many2one('res.users', copy=False)

    def check_activity(self):
        today = datetime.today().date()
        for employee in self.search([]):
            msg_body = "Employee Activity Notification  " + "<br/>"
            # msg_body += "Please Check order %s  " % order.name + "<br/>"
            activities = self.env['mail.activity'].search(
                [('res_model', '=', 'hr.employee'), ('res_id', '=', employee.id)])
            for activity in activities:
                if (
                        today - activity.date_deadline).days <= employee.company_id.employee_send_email_action_before and employee.company_id.employee_send_email_action_before:
                    email_user = activity.user_id
                    partner = email_user.partner_id

                    if partner:
                        partner.message_post(message_type='email', body=msg_body, partner_ids=[partner.id])
                    employee_employee_parent_id = employee.user_id.employee_parent_id
                    if employee_employee_parent_id.user_id:
                        employee.email_user = employee_employee_parent_id.user_id.id
                else:
                    email_user = activity.user_id
                    partner = email_user.partner_id
                    if partner:
                        partner.message_post(message_type='email', body=msg_body, partner_ids=[partner.id])
                    employee_employee_parent_id = employee.email_user.employee_parent_id or employee.user_id.employee_parent_id
                    if employee_employee_parent_id.user_id:
                        employee.email_user = employee_employee_parent_id.user_id.id
