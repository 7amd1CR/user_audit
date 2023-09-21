from odoo import api, models, fields
from datetime import datetime
from odoo.http import request


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    email_user = fields.Many2one('res.users', copy=False)

    # -----------CREATE-----------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        result = super().create(vals_list)
        values = {
            'record': result.id,
            'date': result.create_date,
            'user_id': result.create_uid.id,
            'type': 'create',
            'object': result._description,
        }
        self.env['user.audit.log'].sudo().create(values)
        return result

    # -----------WRITE-----------------------------------------------------------------------
    def write(self, vals):
        fields = self.env['ir.model.fields'].sudo().search([('model_id.model', '=', self._name)])
        for field in fields:
            for lead in vals:
                if field.name == lead:
                    old_value = self[field.name]
                    values = {
                        'record': self.id,
                        'date': self.write_date,
                        'user_id': self.write_uid.id,
                        'type': 'write',
                        'object': self._description,
                        'update_field': lead,
                        'updated_value': str(vals[lead]),
                        'old_value': str(old_value),
                    }
                    self.env['user.audit.log'].sudo().create(values)
        return super(CrmLead, self).write(vals)

    # -----------READ-----------------------------------------------------------------------
    def read(self, fields=None, load='_classic_read'):
        result = super(CrmLead, self).read(fields, load=load)
        # print('read',result)
        values = {
            'record': result[0]['id'],
            'date': datetime.now(),
            'user_id': self.env.user.id,
            'type': 'read',
            'object': self._description,
        }
        self.env['user.audit.log'].sudo().create(values)
        return result

    #
    # # -----------UNLINK-----------------------------------------------------------------------
    def unlink(self):
        for lead in self:
            values = {
                'record': lead.id,
                'date': datetime.now(),
                'user_id': lead.env.user.id,
                'type': 'delete',
                'object': lead._description
            }
            self.env['user.audit.log'].sudo().create(values)
        return super().unlink()

    # -----------COPY-----------------------------------------------------------------------
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        result = super().copy(default=default)
        for rec in self:
            values = {
                'record': rec.id,
                'date': datetime.now(),
                'user_id': rec.env.user.id,
                'type': 'copy',
                'object': rec._description
            }
            self.env['user.audit.log'].sudo().create(values)
        return result

    # -----------Schedule Activity----------------------------------------------------------------------

    def check_activity(self):
        today = datetime.today().date()
        for lead in self.search([]):
            msg_body = "Crm Activity Notification  " + "<br/>"
            msg_body += "Please Check lead or opportunity %s  " % lead.name + "<br/>"

            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url = base_url + '/web#id=%d&view_type=form&model=%s' % (lead.id, lead._name)
            msg_body += "Link:  %s  " % url + "<br/>"

            activities = self.env['mail.activity'].search([('res_model', '=', 'crm.lead'), ('res_id', '=', lead.id)])
            for activity in activities:
                if (
                        today - activity.date_deadline).days <= lead.company_id.crm_send_email_action_before and lead.company_id.crm_send_email_action_before:
                    email_user = activity.user_id
                    partner = email_user.partner_id
                    if partner:
                        partner.message_post(message_type='email', body=msg_body, partner_ids=[partner.id])
                    lead_employee_parent_id = lead.user_id.employee_parent_id
                    if lead_employee_parent_id.user_id:
                        lead.email_user = lead_employee_parent_id.user_id.id
                else:
                    email_user = lead.email_user
                    partner = email_user.partner_id
                    if partner:
                        partner.message_post(message_type='email', body=msg_body, partner_ids=[partner.id])
                    lead_employee_parent_id = lead.email_user.employee_parent_id or lead.user_id.employee_parent_id
                    if lead_employee_parent_id.user_id:
                        lead.email_user = lead_employee_parent_id.user_id.id
