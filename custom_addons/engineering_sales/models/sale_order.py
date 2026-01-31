from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        
        new_project = self.env['project.project']
        for order in self:
            # We are keeping the safe project creation logic
            new_project |= self.env['project.project'].with_context(
                sale_project_skip_create_project=True
            ).create({
                'name': order.name,
                'partner_id': order.partner_id.id,
            })

        # # --- THE NEW REDIRECT LOGIC ---
        # if len(new_project) == 1:
        #     return {
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'project.project',
        #         'view_mode': 'form',
        #         'res_id': new_project.id,
        #     }
        
        return res