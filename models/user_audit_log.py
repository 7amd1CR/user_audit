from odoo import api, fields, models


class UserAuditLog(models.Model):
    _name = 'user.audit.log'
    _rec_name = 'update_field'

    reference = fields.Char(readonly=True)
    user_id = fields.Many2one('res.users')
    record = fields.Integer(string='Record Id')
    object = fields.Char(string='Object')
    type = fields.Selection(
        [('read', 'Read'), ('write', 'Write'), ('create', 'Create'), ('delete', 'Delete'), ('copy', 'Copy')])
    date = fields.Datetime(string='Date')
    update_field = fields.Char(string='Update field')

    updated_value = fields.Char(string='Updated Value')
    old_value = fields.Char(string='Old Value')

