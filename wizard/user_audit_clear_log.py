from odoo import api, models, fields
from odoo.exceptions import ValidationError


class ClearLog(models.TransientModel):
    _name = 'user.audit.clear.log'

    all_log = fields.Boolean(string='All Log')
    to_date = fields.Date(string='To Date', required=True)
    type = fields.Selection(
        selection=[('read', 'Read'), ('write', 'Write'), ('create', 'Create'), ('delete', 'Delete')])

    # ----------------------------------------------------------------------------------------------------------
    def clear_log(self):
        if self.all_log == True:
            self.env['user.audit.log'].search([]).unlink()
        else:
            if not self.type:
                raise ValidationError("Select The Type Action")
            else:
                self.env['user.audit.log'].search(
                    [('date', '<', self.to_date), ('type', '=', self.type)]).unlink()
