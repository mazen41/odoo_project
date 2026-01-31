from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    active = fields.Boolean(default=True)

    def unlink(self):
        for rec in self:
            # archive instead of delete
            rec.active = False
        return True
